import speech_recognition as sr
import json
import time
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, or_
from models import Base, Recipe, Ingredient
import subprocess
from difflib import SequenceMatcher
from indian_recipes import (
    INDIAN_RECIPES,
    get_recipe_by_name,
    get_recipes_by_cuisine,
    get_recipes_by_diet,
    get_recipes_by_difficulty,
    get_recipes_by_max_time
)
from openai import OpenAI
from typing import List, Dict, Any, Optional, Tuple
import os
from dotenv import load_dotenv
import logging
import random
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import functools
from datetime import datetime, timedelta
import threading
import queue
import concurrent.futures
import sys

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
try:
    client = OpenAI(api_key=api_key)
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    client = None

# Rate limiting configuration
API_CALLS = {}
MAX_CALLS_PER_MINUTE = 20
RATE_LIMIT_WINDOW = 60  # seconds

def check_rate_limit():
    """Check if we've exceeded API rate limits"""
    current_time = time.time()
    # Clean up old entries
    API_CALLS.update({k: v for k, v in API_CALLS.items() if current_time - k < RATE_LIMIT_WINDOW})
    # Count recent calls
    recent_calls = sum(1 for k in API_CALLS.keys() if current_time - k < RATE_LIMIT_WINDOW)
    if recent_calls >= MAX_CALLS_PER_MINUTE:
        return False
    API_CALLS[current_time] = True
    return True

class CognitiveSpeech:
    """Handles natural language generation and conversation flow"""
    
    def __init__(self):
        self.conversation_history = []
        self.greeting_patterns = [
            "Hi! I'm your cooking buddy. What would you like to cook today?",
            "Hello! Ready to make something delicious?",
            "Welcome to your kitchen assistant! What shall we cook?",
            "Hey there! I'm here to help you cook something amazing!"
        ]
        self.acknowledgments = [
            "I understand you want to make",
            "Ah, you'd like to cook",
            "Great choice! Let's make",
            "Excellent! I can help you with"
        ]
        self.transitions = [
            "Now, let's move on to",
            "Next up is",
            "Let's continue with",
            "Moving forward with"
        ]
        self.encouragements = [
            "You're doing great!",
            "That's perfect!",
            "Excellent progress!",
            "You're nailing it!"
        ]
        self.error_responses = [
            "I didn't quite catch that. Could you please repeat?",
            "Sorry, I'm having trouble understanding. Can you say that again?",
            "I missed what you said. One more time, please?",
            "Could you rephrase that for me?"
        ]

    def get_greeting(self) -> str:
        return random.choice(self.greeting_patterns)

    def get_acknowledgment(self, recipe_name: str) -> str:
        return f"{random.choice(self.acknowledgments)} {recipe_name}!"

    def get_transition(self) -> str:
        return random.choice(self.transitions)

    def get_encouragement(self) -> str:
        return random.choice(self.encouragements)

    def get_error_response(self) -> str:
        return random.choice(self.error_responses)

    def format_recipe_introduction(self, recipe: Dict[str, Any]) -> str:
        """Creates a natural introduction for a recipe"""
        intro = f"I found a wonderful recipe for {recipe['name']}. "
        intro += f"This is a {recipe['cuisine_type']} dish "
        if 'difficulty_level' in recipe:
            intro += f"with a {recipe['difficulty_level']} difficulty level. "
        if 'preparation_time' in recipe:
            intro += f"It takes about {recipe['preparation_time']} minutes to prepare. "
        return intro

    def format_step_instruction(self, step_num: int, step: Dict[str, Any]) -> str:
        """Creates a natural instruction for a recipe step"""
        instruction = f"Step {step_num}: {step['step']}. "
        if step.get('time', 0) > 0:
            instruction += f"This will take about {step['time']} minutes. "
        return instruction

class Cache:
    def __init__(self, max_size: int = 100, ttl_minutes: int = 60):
        self.cache = {}
        self.max_size = max_size
        self.ttl = timedelta(minutes=ttl_minutes)
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if datetime.now() - item['timestamp'] < self.ttl:
                    return item['value']
                else:
                    del self.cache[key]
            return None

    def set(self, key: str, value: Any):
        with self.lock:
            if len(self.cache) >= self.max_size:
                # Remove oldest items
                oldest = sorted(self.cache.items(), key=lambda x: x[1]['timestamp'])[0][0]
                del self.cache[oldest]
            self.cache[key] = {
                'value': value,
                'timestamp': datetime.now()
            }

class RecipeExtractor:
    def __init__(self):
        self.client = client
        self.local_cache = {}

    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=4),
        retry=retry_if_exception_type(Exception)
    )
    def extract_recipe_name(self, user_input: str) -> str:
        """Extract recipe name from user input using AI with improved fallback"""
        # First check local cache
        if user_input.lower() in self.local_cache:
            return self.local_cache[user_input.lower()]

        # Try traditional extraction first
        recipe_name = self._traditional_extract(user_input)
        
        # If we have a clear recipe name from traditional extraction, use it
        if recipe_name and len(recipe_name.split()) <= 3:
            self.local_cache[user_input.lower()] = recipe_name
            return recipe_name

        # Only use AI if available and rate limit allows
        if self.client and check_rate_limit():
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a recipe name extractor. Extract only the recipe name from the user's input. Respond with ONLY the recipe name, nothing else."},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.3,
                    max_tokens=50
                )
                recipe_name = response.choices[0].message.content.strip()
                self.local_cache[user_input.lower()] = recipe_name
                return recipe_name
            except Exception as e:
                logger.error(f"AI extraction failed: {e}")
                return self._traditional_extract(user_input)
        
        return recipe_name

    def _traditional_extract(self, user_input: str) -> str:
        """Enhanced traditional rule-based recipe name extraction"""
        user_input = user_input.lower()
        
        # Common recipe request patterns
        patterns = [
            "recipe for",
            "how to make",
            "how do i make",
            "cook",
            "prepare",
            "can you help me make",
            "show me how to make",
            "i want to make"
        ]
        
        # Try to extract recipe name using patterns
        for pattern in patterns:
            if pattern in user_input:
                recipe_name = user_input.split(pattern)[-1].strip()
                # Clean up common words
                for word in ["a", "an", "the", "some"]:
                    recipe_name = recipe_name.replace(f" {word} ", " ")
                return recipe_name.strip()
        
        # If no pattern matches, try to find the recipe in our database
        for recipe in INDIAN_RECIPES.values():
            if recipe["name"].lower() in user_input:
                return recipe["name"]
        
        # If all else fails, return cleaned input
        return ' '.join(word for word in user_input.split() 
                       if word not in ["recipe", "make", "cook", "how", "to", "can", "you", "help", "me"])

class ParallelRecipeFetcher:
    def __init__(self, recipe_manager):
        self.recipe_manager = recipe_manager
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        self.result_queue = queue.Queue()

    def fetch_recipe_parallel(self, recipe_name: str) -> Tuple[Dict[str, Any], str]:
        """Fetch recipe from both database and API in parallel"""
        def local_search():
            start_time = time.time()
            result = self.recipe_manager._get_local_recipe(recipe_name)
            if result:
                self.result_queue.put(("local", result, time.time() - start_time))

        def api_search():
            if client:
                start_time = time.time()
                result = self.recipe_manager._get_recipe_from_api(recipe_name)
                if result:
                    self.result_queue.put(("api", result, time.time() - start_time))

        # Start both searches in parallel
        future_local = self.executor.submit(local_search)
        future_api = self.executor.submit(api_search)

        # Wait for first result or timeout after 5 seconds
        try:
            source, recipe, duration = self.result_queue.get(timeout=5)
            logger.info(f"Recipe found from {source} in {duration:.2f} seconds")
            return recipe, source
        except queue.Empty:
            logger.warning("No recipe found in time")
            return None, None
        finally:
            # Cancel remaining searches
            future_local.cancel()
            future_api.cancel()

class RecipeManager:
    def __init__(self):
        self.recipes = INDIAN_RECIPES
        self.recipe_cache = Cache(max_size=100, ttl_minutes=60)
        self.api_cache = Cache(max_size=50, ttl_minutes=30)
        self.recipe_extractor = RecipeExtractor()
        self.parallel_fetcher = None  # Will be initialized later
        self.context = {
            "current_recipe": None,
            "last_search": None,
            "search_results": [],
            "available_ingredients": [],
            "cooking_stage": None,
            "dietary_restrictions": [],
            "cuisine_preference": None
        }
        self.recipe_index = self._build_recipe_index()
        
    def initialize_parallel_fetcher(self):
        """Initialize parallel fetcher after self is fully initialized"""
        self.parallel_fetcher = ParallelRecipeFetcher(self)

    def _build_recipe_index(self) -> Dict[str, set]:
        """Build an inverted index for faster recipe search"""
        index = {
            'ingredients': {},
            'cuisine_types': {},
            'difficulty_levels': {}
        }
        
        for recipe_id, recipe in self.recipes.items():
            # Index ingredients
            for ingredient in recipe['ingredients']:
                ing_name = ingredient['name'].lower()
                if ing_name not in index['ingredients']:
                    index['ingredients'][ing_name] = set()
                index['ingredients'][ing_name].add(recipe_id)
            
            # Index cuisine types
            cuisine = recipe['cuisine_type'].lower()
            if cuisine not in index['cuisine_types']:
                index['cuisine_types'][cuisine] = set()
            index['cuisine_types'][cuisine].add(recipe_id)
            
            # Index difficulty levels
            difficulty = recipe['difficulty_level'].lower()
            if difficulty not in index['difficulty_levels']:
                index['difficulty_levels'][difficulty] = set()
            index['difficulty_levels'][difficulty].add(recipe_id)
        
        return index

    @functools.lru_cache(maxsize=128)
    def _fuzzy_match_score(self, str1: str, str2: str) -> float:
        """Cached fuzzy matching for strings"""
        return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

    def process_user_query(self, user_input: str) -> Tuple[Dict[str, Any], str]:
        """Process user query with improved error handling and fallback"""
        try:
            # Extract recipe name
            recipe_name = self.recipe_extractor.extract_recipe_name(user_input)
            logger.info(f"Extracted recipe name: {recipe_name}")
            
            # Update context
            self.context["last_search"] = recipe_name
            
            # Check cache first
            cached_recipe = self.recipe_cache.get(recipe_name.lower())
            if cached_recipe:
                return cached_recipe, "cache"
            
            # Try local database first
            local_recipe = self._get_local_recipe(recipe_name)
            if local_recipe:
                self.recipe_cache.set(recipe_name.lower(), local_recipe)
                return local_recipe, "local"
            
            # Initialize parallel fetcher if needed
            if not self.parallel_fetcher:
                self.initialize_parallel_fetcher()
            
            # Try parallel search with timeout
            recipe, source = self.parallel_fetcher.fetch_recipe_parallel(recipe_name)
            if recipe:
                self.recipe_cache.set(recipe_name.lower(), recipe)
                return recipe, source
            
            # If no exact match found, try fuzzy matching
            similar_recipes = self.find_similar_recipes(recipe_name)
            if similar_recipes:
                self.context["search_results"] = similar_recipes
                return similar_recipes[0], "similar"
            
            return None, None
            
        except Exception as e:
            logger.error(f"Error in process_user_query: {e}")
            return None, None

    def find_similar_recipes(self, recipe_name: str, threshold: float = 0.6) -> List[Dict[str, Any]]:
        """Find similar recipes using fuzzy matching"""
        similar_recipes = []
        for recipe in self.recipes.values():
            ratio = SequenceMatcher(None, recipe_name.lower(), recipe["name"].lower()).ratio()
            if ratio > threshold:
                recipe_copy = recipe.copy()
                recipe_copy["match_score"] = ratio
                similar_recipes.append(recipe_copy)
        
        return sorted(similar_recipes, key=lambda x: x["match_score"], reverse=True)

    def get_recipe_details(self, recipe_name: str) -> Tuple[Dict[str, Any], bool]:
        """Get recipe details from cache, local database, or API"""
        # Check cache first
        cached_recipe = self.recipe_cache.get(recipe_name.lower())
        if cached_recipe:
            return cached_recipe, True

        # Try local database with exact and fuzzy matching
        local_recipe = self._get_local_recipe(recipe_name)
        if local_recipe:
            self.recipe_cache.set(recipe_name.lower(), local_recipe)
            return local_recipe, True

        # If not found locally and API is available, try API
        if client:
            api_recipe = self._get_recipe_from_api(recipe_name)
            if api_recipe:
                self.recipe_cache.set(recipe_name.lower(), api_recipe)
                return api_recipe, False

        return None, False

    def _get_local_recipe(self, recipe_name: str) -> Optional[Dict[str, Any]]:
        """Get recipe from local database with optimized search"""
        # Try exact match first (O(1) operation)
        for recipe in self.recipes.values():
            if recipe["name"].lower() == recipe_name.lower():
                return recipe
        
        # If no exact match, try fuzzy matching with threshold
        best_match = None
        highest_ratio = 0
        
        # Use only the first word for initial filtering
        first_word = recipe_name.lower().split()[0]
        candidates = [r for r in self.recipes.values() 
                     if first_word in r["name"].lower()]
        
        # Perform fuzzy matching only on filtered candidates
        for recipe in candidates:
            ratio = self._fuzzy_match_score(recipe_name, recipe["name"])
            if ratio > highest_ratio and ratio > 0.6:
                highest_ratio = ratio
                best_match = recipe
        
        return best_match

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _get_recipe_from_api(self, recipe_name: str) -> Optional[Dict[str, Any]]:
        """Get recipe from OpenAI API with improved rate limiting"""
        if not check_rate_limit():
            logger.warning("API rate limit reached, using local database")
            return None
            
        try:
            # Check API cache first
            cached_response = self.api_cache.get(recipe_name.lower())
            if cached_response:
                return cached_response

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a cooking expert. Provide recipe details in JSON format."},
                    {"role": "user", "content": f"Provide a detailed recipe for {recipe_name} in JSON format with name, ingredients (with quantities), steps, cuisine_type, preparation_time, and difficulty_level."}
                ],
                temperature=0.7,
                max_tokens=500
            )

            try:
                recipe_data = json.loads(response.choices[0].message.content)
                self.api_cache.set(recipe_name.lower(), recipe_data)
                return recipe_data
            except json.JSONDecodeError:
                logger.error("Failed to parse API response as JSON")
                return None

        except Exception as e:
            logger.error(f"API error: {str(e)}")
            return None

    def get_recipe_suggestions(self, ingredients: List[str] = None, cuisine: str = None) -> List[Dict[str, Any]]:
        """Get recipe suggestions using indexed search"""
        matching_recipes = set()
        
        if ingredients:
            # Find recipes matching ingredients using index
            for ingredient in ingredients:
                ing_matches = set()
                for indexed_ing in self.recipe_index['ingredients']:
                    if self._fuzzy_match_score(ingredient, indexed_ing) > 0.6:
                        ing_matches.update(self.recipe_index['ingredients'][indexed_ing])
                
                if not matching_recipes:
                    matching_recipes = ing_matches
                else:
                    matching_recipes &= ing_matches
        
        if cuisine:
            # Filter by cuisine using index
            cuisine_matches = set()
            for indexed_cuisine in self.recipe_index['cuisine_types']:
                if self._fuzzy_match_score(cuisine, indexed_cuisine) > 0.6:
                    cuisine_matches.update(self.recipe_index['cuisine_types'][indexed_cuisine])
            
            if matching_recipes:
                matching_recipes &= cuisine_matches
            else:
                matching_recipes = cuisine_matches
        
        if not matching_recipes and not ingredients and not cuisine:
            # If no filters, return all recipes
            matching_recipes = set(self.recipes.keys())
        
        # Convert recipe IDs to full recipes and calculate scores
        scored_recipes = []
        for recipe_id in matching_recipes:
            recipe = self.recipes[recipe_id]
            score = self._calculate_recipe_score(recipe, ingredients, cuisine)
            scored_recipes.append({
                "name": recipe["name"],
                "score": score,
                "cuisine": recipe["cuisine_type"],
                "description": recipe["description"],
                "difficulty": recipe["difficulty_level"],
                "time": recipe["preparation_time"]
            })
        
        # Sort by score and return top 5
        return sorted(scored_recipes, key=lambda x: x["score"], reverse=True)[:5]

    def _calculate_recipe_score(self, recipe: Dict[str, Any], ingredients: List[str] = None, cuisine: str = None) -> float:
        """Calculate recipe match score based on multiple factors"""
        score = 50.0  # Base score
        
        if ingredients:
            matching_ingredients = sum(
                max(self._fuzzy_match_score(ing, recipe_ing["name"])
                    for recipe_ing in recipe["ingredients"])
                for ing in ingredients
            )
            score += (matching_ingredients / len(ingredients)) * 30
        
        if cuisine and self._fuzzy_match_score(cuisine, recipe["cuisine_type"]) > 0.6:
            score += 20
            
        # Adjust score based on difficulty
        difficulty_weights = {"easy": 1.1, "medium": 1.0, "hard": 0.9}
        score *= difficulty_weights.get(recipe["difficulty_level"].lower(), 1.0)
        
        return score

class VoiceCookingAssistant:
    def __init__(self):
        # Initialize speech recognition with error recovery
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.operation_timeout = 30  # Timeout for operations
        
        # Set up database connection with retry
        try:
            engine = create_engine('sqlite:///cooking_assistant.db')
            Session = sessionmaker(bind=engine)
            self.session = Session()
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise

        # Initialize components
        self.recipe_manager = RecipeManager()
        self.cognitive_speech = CognitiveSpeech()
        self.last_error_time = 0
        self.error_count = 0
        self.max_consecutive_errors = 3

    def speak(self, text: str):
        """Enhanced text-to-speech with error handling"""
        try:
            print(f"Assistant: {text}")
            # Use only Samantha voice for consistency
            subprocess.run(['say', '-v', 'Samantha', '-r', '180', text], 
                         check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Speech synthesis failed: {e}")
            print(f"Assistant (text only): {text}")
        except Exception as e:
            logger.error(f"Unexpected error in speak: {e}")
            print(f"Assistant (text only): {text}")

    def listen(self) -> Optional[str]:
        """Enhanced voice input with error recovery"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                # Dynamic noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Adjusted for ambient noise. Please speak now...")
                
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    print("Processing your speech...")
                except sr.WaitTimeoutError:
                    self.speak(self.cognitive_speech.get_error_response())
                    return None

                try:
                    text = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"You said: {text}")
                    # Reset error count on successful recognition
                    self.error_count = 0
                    return text.lower()
                except sr.UnknownValueError:
                    self.error_count += 1
                    if self.error_count >= self.max_consecutive_errors:
                        self.speak("I'm having trouble understanding. Let's start over.")
                        self.error_count = 0
                        return None
                    self.speak(self.cognitive_speech.get_error_response())
                    return None
                except sr.RequestError as e:
                    logger.error(f"Speech recognition service error: {e}")
                    self.speak("There seems to be an issue with the speech recognition service. Please try again.")
                    return None

        except Exception as e:
            current_time = time.time()
            if current_time - self.last_error_time > 60:  # Reset error count after 1 minute
                self.error_count = 0
            self.last_error_time = current_time
            
            self.error_count += 1
            logger.error(f"Error during speech recognition: {e}")
            
            if self.error_count >= self.max_consecutive_errors:
                self.speak("I'm having technical difficulties. Please check your microphone and try again.")
                self.error_count = 0
            return None

    def process_recipe_request(self, user_input: str):
        """Process recipe requests with enhanced interaction"""
        try:
            # Extract recipe name
            recipe_name = self.recipe_manager.recipe_extractor._traditional_extract(user_input)
            
            # Acknowledge the request
            self.speak(self.cognitive_speech.get_acknowledgment(recipe_name))
            
            # Try local database first
            local_recipe = self.recipe_manager._get_local_recipe(recipe_name)
            
            if local_recipe:
                # Use cognitive speech for introduction
                intro = self.cognitive_speech.format_recipe_introduction(local_recipe)
                self.speak(intro)
                
                # List ingredients with natural transitions
                self.speak(f"{self.cognitive_speech.get_transition()} the ingredients you'll need:")
                for ingredient in local_recipe['ingredients']:
                    self.speak(f"{ingredient['quantity']} {ingredient['unit']} of {ingredient['name']}")
                
                # Ask about starting cooking
                self.speak("Would you like to start cooking this recipe? Say yes when you're ready.")
                response = self.listen()
                
                if response and 'yes' in response:
                    self.guide_cooking(local_recipe)
                else:
                    self.speak("No problem! Let me know when you want to try this or another recipe.")
                return

            # If not found locally, try API with cognitive interaction
            if client:
                self.speak("Let me search online for that recipe...")
                try:
                    recipe_name = self.recipe_manager.recipe_extractor.extract_recipe_name(user_input)
                    api_recipe = self.recipe_manager._get_recipe_from_api(recipe_name)
                    
                    if api_recipe:
                        intro = self.cognitive_speech.format_recipe_introduction(api_recipe)
                        self.speak(intro)
                        
                        self.speak(f"{self.cognitive_speech.get_transition()} the ingredients:")
                        for ingredient in api_recipe['ingredients']:
                            self.speak(f"{ingredient['quantity']} {ingredient['unit']} of {ingredient['name']}")
                        
                        self.speak("Would you like to start cooking? Just say yes when you're ready.")
                        response = self.listen()
                        
                        if response and 'yes' in response:
                            self.guide_cooking(api_recipe)
                        else:
                            self.speak("That's fine! Let me know if you want to try this or another recipe later.")
                        return
                except Exception as e:
                    logger.error(f"API error: {e}")
                    # Continue to suggestions

            # Offer suggestions with cognitive interaction
            self.speak("I couldn't find that exact recipe, but I might have something similar you'd like.")
            self.speak("Would you like to hear some suggestions?")
            response = self.listen()
            
            if response and 'yes' in response:
                suggestions = self.recipe_manager.get_recipe_suggestions()
                self.speak("Here are some recipes I think you might enjoy:")
                for suggestion in suggestions[:3]:
                    self.speak(f"{suggestion['name']}: {suggestion['description']}")
                    time.sleep(1)  # Pause between suggestions

        except Exception as e:
            logger.error(f"Error in process_recipe_request: {e}")
            self.speak("I encountered an issue while processing your request. Let's try again.")

    def guide_cooking(self, recipe: Dict[str, Any]):
        """Guide through cooking with cognitive interaction"""
        try:
            self.speak(f"Great! Let's cook {recipe['name']} together!")
            self.speak(self.cognitive_speech.get_encouragement())
            
            # Go through each step
            for i, step in enumerate(recipe['steps'], 1):
                instruction = self.cognitive_speech.format_step_instruction(i, step)
                self.speak(instruction)
                
                if step.get('time', 0) > 0:
                    self.speak("Let me know when you're ready for the next step by saying 'next' or 'continue'.")
                    self.speak("You can also say 'repeat' to hear this step again, or 'stop' to pause the recipe.")
                
                while True:
                    response = self.listen()
                    if response:
                        if 'next' in response or 'continue' in response:
                            self.speak(self.cognitive_speech.get_encouragement())
                            break
                        elif 'repeat' in response:
                            self.speak("Sure, let me repeat that step for you.")
                            self.speak(instruction)
                        elif 'stop' in response or 'quit' in response:
                            self.speak("Okay, we'll pause here. You can resume this recipe later.")
                            return
                
            self.speak(f"Congratulations! You've completed {recipe['name']}!")
            self.speak("I hope it turns out delicious. Would you like to try another recipe?")

        except Exception as e:
            logger.error(f"Error in guide_cooking: {e}")
            self.speak("I encountered an issue while guiding you. Let's start over.")

    def run(self):
        """Main loop with enhanced cognitive interaction"""
        try:
            self.speak(self.cognitive_speech.get_greeting())
            self.speak("You can ask me about any recipe, like 'How do I make butter chicken?' or say 'suggest recipes' for ideas.")
            
            while True:
                user_input = self.listen()
                if user_input:
                    if 'exit' in user_input or 'quit' in user_input or 'stop' in user_input:
                        self.speak("Thanks for cooking with me today! Come back when you're ready to make something delicious!")
                        break
                    elif any(phrase in user_input for phrase in ['recipe', 'how to make', 'cook', 'make']):
                        self.process_recipe_request(user_input)
                    elif 'suggest' in user_input:
                        suggestions = self.recipe_manager.get_recipe_suggestions()
                        self.speak("I've got some great recipes for you!")
                        for suggestion in suggestions[:3]:
                            self.speak(f"{suggestion['name']}: {suggestion['description']}")
                            time.sleep(1)
                    else:
                        self.speak("I'm not sure what you'd like to do. You can ask me how to make any dish, or say 'suggest recipes' for ideas.")

        except KeyboardInterrupt:
            self.speak("Goodbye! Have a great day!")
        except Exception as e:
            logger.error(f"Critical error in main loop: {e}")
            self.speak("I'm having technical difficulties. Please restart the assistant.")

if __name__ == "__main__":
    try:
        assistant = VoiceCookingAssistant()
        assistant.run()
    except Exception as e:
        logger.error(f"Failed to start assistant: {e}")
        print("Error: Failed to start the cooking assistant. Please check the logs.")