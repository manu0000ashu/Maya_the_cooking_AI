from flask import Flask, render_template, request, jsonify
from main import VoiceCookingAssistant, RecipeManager
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)
load_dotenv()

# Initialize the cooking assistant
recipe_manager = RecipeManager()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search_recipe', methods=['POST'])
def search_recipe():
    try:
        data = request.json
        query = data.get('query', '')
        ingredients = data.get('ingredients', [])
        
        # Update recipe manager with ingredients
        recipe_manager.context['available_ingredients'] = ingredients
        
        # Search for recipe
        recipe, source = recipe_manager.process_user_query(query)
        
        if recipe:
            return jsonify({
                'success': True,
                'recipe': recipe,
                'source': source
            })
        else:
            # Get suggestions if exact match not found
            suggestions = recipe_manager.get_recipe_suggestions(ingredients=ingredients)
            return jsonify({
                'success': True,
                'suggestions': suggestions[:5]  # Return top 5 suggestions
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/suggest_recipes', methods=['POST'])
def suggest_recipes():
    try:
        data = request.json
        ingredients = data.get('ingredients', [])
        cuisine = data.get('cuisine', None)
        
        suggestions = recipe_manager.get_recipe_suggestions(
            ingredients=ingredients,
            cuisine=cuisine
        )
        
        return jsonify({
            'success': True,
            'suggestions': suggestions[:5]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recipe_details/<recipe_name>')
def recipe_details(recipe_name):
    try:
        recipe, is_local = recipe_manager.get_recipe_details(recipe_name)
        if recipe:
            return jsonify({
                'success': True,
                'recipe': recipe,
                'is_local': is_local
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Recipe not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=8081) 