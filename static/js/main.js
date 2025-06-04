// Initialize variables
let ingredients = [];
let recognition;
let speechSynthesis = window.speechSynthesis;
let currentlySpeaking = false;

// Check if browser supports speech recognition
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
} else {
    $('#startVoice').prop('disabled', true);
    $('#startVoice').attr('title', 'Voice recognition not supported in this browser');
}

// DOM Ready
$(document).ready(function() {
    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Add ingredient
    $('#addIngredient').click(function() {
        addIngredient();
    });

    // Handle enter key on ingredient input
    $('#ingredientInput').keypress(function(e) {
        if (e.which == 13) {
            addIngredient();
        }
    });

    // Search button click
    $('#searchButton').click(function() {
        searchRecipe();
    });

    // Recipe search enter key
    $('#recipeSearch').keypress(function(e) {
        if (e.which == 13) {
            searchRecipe();
        }
    });

    // Find recipes button
    $('#findRecipes').click(function() {
        findRecipesByIngredients();
    });

    // Voice search button
    $('#startVoice').click(function() {
        startVoiceRecognition();
    });
});

// Add ingredient function
function addIngredient() {
    const ingredient = $('#ingredientInput').val().trim();
    if (ingredient && !ingredients.includes(ingredient)) {
        ingredients.push(ingredient);
        const tag = $('<div>')
            .addClass('ingredient-tag')
            .html(`${ingredient} <i class="fas fa-times"></i>`);
        
        tag.find('i').click(function() {
            const index = ingredients.indexOf(ingredient);
            if (index > -1) {
                ingredients.splice(index, 1);
            }
            tag.remove();
        });

        $('#ingredientsList').append(tag);
        $('#ingredientInput').val('');
    }
}

// Search recipe function
function searchRecipe() {
    const query = $('#recipeSearch').val().trim();
    if (!query) return;

    showLoading('#recipeDisplay');
    
    $.ajax({
        url: '/api/search_recipe',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            query: query,
            ingredients: ingredients
        }),
        success: function(response) {
            if (response.success) {
                if (response.recipe) {
                    displayRecipe(response.recipe);
                } else if (response.suggestions) {
                    displaySuggestions(response.suggestions);
                }
            } else {
                showError('No recipes found');
            }
        },
        error: function() {
            showError('Error searching for recipe');
        }
    });
}

// Find recipes by ingredients
function findRecipesByIngredients() {
    if (ingredients.length === 0) {
        showError('Please add some ingredients first');
        return;
    }

    showLoading('#recipeDisplay');
    
    $.ajax({
        url: '/api/suggest_recipes',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            ingredients: ingredients,
            cuisine: $('#cuisineFilter').val()
        }),
        success: function(response) {
            if (response.success && response.suggestions) {
                displaySuggestions(response.suggestions);
            } else {
                showError('No recipes found with these ingredients');
            }
        },
        error: function() {
            showError('Error finding recipes');
        }
    });
}

// Display recipe function
function displayRecipe(recipe) {
    const recipeHtml = `
        <div class="recipe-details">
            <h3>${recipe.name}</h3>
            <p class="text-muted">${recipe.cuisine_type} | ${recipe.difficulty_level} | ${recipe.preparation_time} mins</p>
            
            <div class="d-flex justify-content-end mb-3">
                <button class="btn btn-primary" onclick="narrateRecipe(${JSON.stringify(recipe).replace(/"/g, '&quot;')})">
                    <i class="fas fa-volume-up"></i> Narrate Recipe
                </button>
                <button class="btn btn-secondary ms-2" onclick="stopNarration()">
                    <i class="fas fa-stop"></i> Stop Narration
                </button>
            </div>

            <h4>Ingredients</h4>
            <ul class="ingredients-list">
                ${recipe.ingredients.map(ing => 
                    `<li>${ing.quantity} ${ing.unit} ${ing.name}</li>`
                ).join('')}
            </ul>

            <h4>Instructions</h4>
            <ol class="steps-list">
                ${recipe.steps.map(step => 
                    `<li>${step.step}</li>`
                ).join('')}
            </ol>
        </div>
    `;

    $('#recipeDisplay').html(recipeHtml);
}

// Display suggestions function
function displaySuggestions(suggestions) {
    const suggestionsHtml = suggestions.map(recipe => `
        <div class="col-md-4">
            <div class="recipe-grid-item" onclick="getRecipeDetails('${recipe.name}')">
                <div class="card">
                    <div class="card-body">
                        <h5 class="card-title">${recipe.name}</h5>
                        <p class="card-text">${recipe.description}</p>
                        <div class="text-muted">
                            <small>${recipe.cuisine_type} | ${recipe.preparation_time} mins</small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `).join('');

    $('#recipeGrid').html(suggestionsHtml);
}

// Get recipe details
function getRecipeDetails(recipeName) {
    showLoading('#recipeDisplay');
    
    $.ajax({
        url: `/api/recipe_details/${encodeURIComponent(recipeName)}`,
        method: 'GET',
        success: function(response) {
            if (response.success && response.recipe) {
                displayRecipe(response.recipe);
            } else {
                showError('Recipe details not found');
            }
        },
        error: function() {
            showError('Error fetching recipe details');
        }
    });
}

// Voice recognition
function startVoiceRecognition() {
    if (!recognition) return;

    $('#voiceModal').modal('show');
    $('#voiceStatus').text('Listening...');
    $('.fa-microphone').addClass('listening');

    recognition.start();

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        $('#recipeSearch').val(transcript);
        $('#voiceModal').modal('hide');
        $('.fa-microphone').removeClass('listening');
        searchRecipe(); // This will trigger the recipe search immediately
    };

    recognition.onend = function() {
        $('#voiceModal').modal('hide');
        $('.fa-microphone').removeClass('listening');
    };

    recognition.onerror = function(event) {
        $('#voiceModal').modal('hide');
        $('.fa-microphone').removeClass('listening');
        showError('Error with voice recognition');
    };
}

// Narrate recipe function
function narrateRecipe(recipe) {
    // Stop any ongoing narration
    stopNarration();
    
    // Create the narration text
    const introText = `Recipe for ${recipe.name}. This is a ${recipe.cuisine_type} dish with ${recipe.difficulty_level} difficulty level and takes ${recipe.preparation_time} minutes to prepare.`;
    
    const ingredientsText = "Here are the ingredients you'll need: " + 
        recipe.ingredients.map(ing => `${ing.quantity} ${ing.unit} ${ing.name}`).join(', ');
    
    const instructionsText = "Now, let's go through the steps: " + 
        recipe.steps.map((step, index) => `Step ${index + 1}: ${step.step}`).join('. ');

    // Function to speak text
    function speak(text, onEnd = null) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9; // Slightly slower rate for better clarity
        utterance.pitch = 1;
        if (onEnd) {
            utterance.onend = onEnd;
        }
        currentlySpeaking = true;
        speechSynthesis.speak(utterance);
    }

    // Chain the narration
    speak(introText, () => {
        speak(ingredientsText, () => {
            speak(instructionsText, () => {
                currentlySpeaking = false;
            });
        });
    });
}

// Stop narration function
function stopNarration() {
    if (currentlySpeaking) {
        speechSynthesis.cancel();
        currentlySpeaking = false;
    }
}

// Utility functions
function showLoading(selector) {
    $(selector).html('<div class="loading"><i class="fas fa-spinner"></i></div>');
}

function showError(message) {
    const errorHtml = `
        <div class="alert alert-danger" role="alert">
            <i class="fas fa-exclamation-circle"></i> ${message}
        </div>
    `;
    $('#recipeDisplay').html(errorHtml);
} 