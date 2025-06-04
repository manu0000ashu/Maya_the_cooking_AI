"""
This module contains a comprehensive collection of Indian recipes.
Data sourced and adapted from various Indian cuisine datasets.
"""

from difflib import SequenceMatcher

INDIAN_RECIPES = {
    # North Indian Dishes
    "butter_chicken": {
        "name": "Butter Chicken",
        "cuisine_type": "North Indian",
        "preparation_time": 40,
        "description": "Creamy and rich chicken curry in tomato-based gravy",
        "difficulty_level": "Medium",
        "serving_size": 4,
        "ingredients": [
            {"name": "chicken", "quantity": 500, "unit": "grams"},
            {"name": "butter", "quantity": 100, "unit": "grams"},
            {"name": "cream", "quantity": 200, "unit": "ml"},
            {"name": "tomato", "quantity": 4, "unit": "pieces"},
            {"name": "onion", "quantity": 2, "unit": "pieces"},
            {"name": "ginger garlic paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "garam masala", "quantity": 1, "unit": "teaspoon"},
            {"name": "kasuri methi", "quantity": 1, "unit": "teaspoon"}
        ],
        "steps": [
            {"step": "Marinate chicken with yogurt and spices", "time": 30},
            {"step": "Prepare tomato-based gravy", "time": 15},
            {"step": "Cook marinated chicken", "time": 20},
            {"step": "Add butter and cream", "time": 5}
        ]
    },
    
    "dal_makhani": {
        "name": "Dal Makhani",
        "cuisine_type": "North Indian",
        "preparation_time": 45,
        "description": "Creamy black lentils cooked overnight",
        "difficulty_level": "Medium",
        "serving_size": 6,
        "ingredients": [
            {"name": "black lentils", "quantity": 250, "unit": "grams"},
            {"name": "kidney beans", "quantity": 50, "unit": "grams"},
            {"name": "butter", "quantity": 50, "unit": "grams"},
            {"name": "cream", "quantity": 100, "unit": "ml"},
            {"name": "tomato puree", "quantity": 200, "unit": "ml"},
            {"name": "ginger garlic paste", "quantity": 2, "unit": "tablespoons"}
        ],
        "steps": [
            {"step": "Soak lentils and beans overnight", "time": 480},
            {"step": "Pressure cook with spices", "time": 45},
            {"step": "Simmer with butter and cream", "time": 30}
        ]
    },

    # South Indian Dishes
    "masala_dosa": {
        "name": "Masala Dosa",
        "cuisine_type": "South Indian",
        "preparation_time": 30,
        "description": "Crispy rice crepe with spiced potato filling",
        "difficulty_level": "Medium",
        "serving_size": 4,
        "ingredients": [
            {"name": "dosa batter", "quantity": 500, "unit": "ml"},
            {"name": "potato", "quantity": 4, "unit": "pieces"},
            {"name": "onion", "quantity": 2, "unit": "pieces"},
            {"name": "mustard seeds", "quantity": 1, "unit": "teaspoon"},
            {"name": "curry leaves", "quantity": 10, "unit": "pieces"}
        ],
        "steps": [
            {"step": "Prepare potato filling", "time": 20},
            {"step": "Heat dosa tawa", "time": 5},
            {"step": "Spread batter and cook", "time": 3},
            {"step": "Add filling and fold", "time": 2}
        ]
    },

    # Gujarati Dishes
    "dhokla": {
        "name": "Dhokla",
        "cuisine_type": "Gujarati",
        "preparation_time": 30,
        "description": "Steamed fermented rice and chickpea flour cake",
        "difficulty_level": "Medium",
        "serving_size": 6,
        "ingredients": [
            {"name": "gram flour", "quantity": 200, "unit": "grams"},
            {"name": "yogurt", "quantity": 100, "unit": "ml"},
            {"name": "green chili", "quantity": 2, "unit": "pieces"},
            {"name": "mustard seeds", "quantity": 1, "unit": "teaspoon"},
            {"name": "curry leaves", "quantity": 10, "unit": "pieces"}
        ],
        "steps": [
            {"step": "Prepare dhokla batter", "time": 10},
            {"step": "Steam the batter", "time": 15},
            {"step": "Prepare tempering", "time": 5}
        ]
    },

    # Bengali Dishes
    "fish_curry": {
        "name": "Bengali Fish Curry",
        "cuisine_type": "Bengali",
        "preparation_time": 35,
        "description": "Traditional Bengali style fish curry with mustard",
        "difficulty_level": "Medium",
        "serving_size": 4,
        "ingredients": [
            {"name": "fish", "quantity": 500, "unit": "grams"},
            {"name": "mustard paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "turmeric", "quantity": 1, "unit": "teaspoon"},
            {"name": "green chili", "quantity": 4, "unit": "pieces"}
        ],
        "steps": [
            {"step": "Marinate fish", "time": 15},
            {"step": "Prepare mustard gravy", "time": 10},
            {"step": "Cook fish in gravy", "time": 10}
        ]
    },

    # Maharashtrian Dishes
    "vada_pav": {
        "name": "Vada Pav",
        "cuisine_type": "Maharashtrian",
        "preparation_time": 40,
        "description": "Spiced potato fritters in bread roll",
        "difficulty_level": "Medium",
        "serving_size": 4,
        "ingredients": [
            {"name": "potato", "quantity": 4, "unit": "pieces"},
            {"name": "bread rolls", "quantity": 4, "unit": "pieces"},
            {"name": "gram flour", "quantity": 100, "unit": "grams"},
            {"name": "green chili", "quantity": 4, "unit": "pieces"},
            {"name": "garlic", "quantity": 6, "unit": "cloves"}
        ],
        "steps": [
            {"step": "Prepare potato mixture", "time": 20},
            {"step": "Make batter and fry vadas", "time": 15},
            {"step": "Assemble in pav", "time": 5}
        ]
    },

    # Rajasthani Dishes
    "dal_baati": {
        "name": "Dal Baati",
        "cuisine_type": "Rajasthani",
        "preparation_time": 60,
        "description": "Baked wheat balls served with lentil curry",
        "difficulty_level": "Hard",
        "serving_size": 4,
        "ingredients": [
            {"name": "wheat flour", "quantity": 250, "unit": "grams"},
            {"name": "mixed lentils", "quantity": 200, "unit": "grams"},
            {"name": "ghee", "quantity": 100, "unit": "grams"},
            {"name": "spices", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Prepare dough for baati", "time": 15},
            {"step": "Cook lentils", "time": 30},
            {"step": "Bake baatis", "time": 25}
        ]
    },

    # Kerala Dishes
    "kerala_fish_curry": {
        "name": "Kerala Fish Curry",
        "cuisine_type": "Kerala",
        "preparation_time": 45,
        "description": "Spicy fish curry with coconut milk",
        "difficulty_level": "Medium",
        "serving_size": 4,
        "ingredients": [
            {"name": "fish", "quantity": 500, "unit": "grams"},
            {"name": "coconut milk", "quantity": 400, "unit": "ml"},
            {"name": "kokum", "quantity": 4, "unit": "pieces"},
            {"name": "curry leaves", "quantity": 20, "unit": "pieces"}
        ],
        "steps": [
            {"step": "Marinate fish", "time": 15},
            {"step": "Prepare curry base", "time": 20},
            {"step": "Cook fish in curry", "time": 10}
        ]
    },

    # Punjabi Dishes
    "sarson_ka_saag": {
        "name": "Sarson ka Saag",
        "cuisine_type": "Punjabi",
        "preparation_time": 60,
        "description": "Mustard greens curry served with makki roti",
        "difficulty_level": "Medium",
        "serving_size": 6,
        "ingredients": [
            {"name": "mustard greens", "quantity": 500, "unit": "grams"},
            {"name": "spinach", "quantity": 250, "unit": "grams"},
            {"name": "makki flour", "quantity": 200, "unit": "grams"},
            {"name": "ghee", "quantity": 50, "unit": "grams"}
        ],
        "steps": [
            {"step": "Clean and chop greens", "time": 20},
            {"step": "Cook greens until tender", "time": 30},
            {"step": "Prepare makki roti", "time": 20}
        ]
    },

    # Street Food
    "pani_puri": {
        "name": "Pani Puri",
        "cuisine_type": "Street Food",
        "preparation_time": 40,
        "description": "Hollow crispy puris with spicy water and filling",
        "difficulty_level": "Easy",
        "serving_size": 4,
        "ingredients": [
            {"name": "puri", "quantity": 24, "unit": "pieces"},
            {"name": "potato", "quantity": 2, "unit": "pieces"},
            {"name": "chickpeas", "quantity": 100, "unit": "grams"},
            {"name": "mint leaves", "quantity": 50, "unit": "grams"},
            {"name": "tamarind", "quantity": 20, "unit": "grams"}
        ],
        "steps": [
            {"step": "Prepare mint water", "time": 15},
            {"step": "Prepare potato filling", "time": 20},
            {"step": "Assemble and serve", "time": 5}
        ]
    },

    # Add new fish curry recipes
    "goan_fish_curry": {
        "name": "Goan Fish Curry",
        "cuisine_type": "Goan",
        "preparation_time": 40,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "A spicy and tangy fish curry from Goa made with coconut milk and Kashmiri chilies",
        "ingredients": [
            {"name": "firm white fish", "quantity": 600, "unit": "grams"},
            {"name": "Kashmiri chili powder", "quantity": 2.5, "unit": "tablespoons"},
            {"name": "coriander powder", "quantity": 1, "unit": "tablespoon"},
            {"name": "cumin powder", "quantity": 2, "unit": "teaspoons"},
            {"name": "turmeric powder", "quantity": 1, "unit": "teaspoon"},
            {"name": "fenugreek powder", "quantity": 0.5, "unit": "teaspoon"},
            {"name": "garlic", "quantity": 6, "unit": "cloves"},
            {"name": "ginger", "quantity": 1, "unit": "tablespoon"},
            {"name": "tamarind paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "coconut milk", "quantity": 400, "unit": "ml"},
            {"name": "onion", "quantity": 1, "unit": "large"},
            {"name": "tomato", "quantity": 2, "unit": "medium"},
            {"name": "curry leaves", "quantity": 10, "unit": "leaves"},
            {"name": "mustard seeds", "quantity": 0.5, "unit": "teaspoon"}
        ],
        "steps": [
            {"step": "Make curry paste by grinding spices with onion, garlic, and ginger", "time": 10},
            {"step": "Fry mustard seeds and curry leaves in oil until fragrant", "time": 2},
            {"step": "Add curry paste and cook until oil separates", "time": 8},
            {"step": "Add tomatoes and coconut milk, simmer until thickened", "time": 10},
            {"step": "Add fish pieces and cook until done", "time": 10}
        ]
    },

    "kerala_fish_molee": {
        "name": "Kerala Fish Molee",
        "cuisine_type": "Kerala",
        "preparation_time": 30,
        "difficulty_level": "Easy",
        "serving_size": 4,
        "description": "A mild and creamy fish curry from Kerala made with coconut milk and minimal spices",
        "ingredients": [
            {"name": "firm white fish", "quantity": 500, "unit": "grams"},
            {"name": "coconut milk", "quantity": 400, "unit": "ml"},
            {"name": "onion", "quantity": 1, "unit": "cup"},
            {"name": "ginger garlic paste", "quantity": 1, "unit": "tablespoon"},
            {"name": "green chilies", "quantity": 2, "unit": "pieces"},
            {"name": "curry leaves", "quantity": 8, "unit": "leaves"},
            {"name": "mustard seeds", "quantity": 1, "unit": "teaspoon"},
            {"name": "turmeric powder", "quantity": 0.5, "unit": "teaspoon"},
            {"name": "black pepper", "quantity": 0.5, "unit": "teaspoon"},
            {"name": "lemon juice", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Marinate fish with turmeric, salt and lemon juice", "time": 10},
            {"step": "Temper mustard seeds and curry leaves in oil", "time": 2}, 
            {"step": "Saute onions until translucent", "time": 5},
            {"step": "Add ginger garlic paste and green chilies", "time": 2},
            {"step": "Pour in coconut milk and simmer", "time": 5},
            {"step": "Add fish and cook until done", "time": 6}
        ]
    },

    "bengali_fish_curry": {
        "name": "Bengali Fish Curry",
        "cuisine_type": "Bengali",
        "preparation_time": 45,
        "difficulty_level": "Medium", 
        "serving_size": 4,
        "description": "A traditional Bengali fish curry made with mustard paste and yogurt",
        "ingredients": [
            {"name": "rohu or catla fish", "quantity": 500, "unit": "grams"},
            {"name": "mustard paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "yogurt", "quantity": 0.5, "unit": "cup"},
            {"name": "onion", "quantity": 2, "unit": "medium"},
            {"name": "tomato", "quantity": 2, "unit": "medium"},
            {"name": "ginger paste", "quantity": 1, "unit": "tablespoon"},
            {"name": "garlic paste", "quantity": 1, "unit": "tablespoon"},
            {"name": "turmeric powder", "quantity": 1, "unit": "teaspoon"},
            {"name": "red chili powder", "quantity": 1, "unit": "teaspoon"},
            {"name": "nigella seeds", "quantity": 0.5, "unit": "teaspoon"},
            {"name": "green chilies", "quantity": 4, "unit": "pieces"}
        ],
        "steps": [
            {"step": "Marinate fish with turmeric and salt", "time": 15},
            {"step": "Fry fish pieces until golden", "time": 8},
            {"step": "Make paste with mustard, yogurt and spices", "time": 5},
            {"step": "Cook onions and tomatoes with spices", "time": 10},
            {"step": "Add mustard-yogurt paste and simmer", "time": 5},
            {"step": "Add fried fish and finish cooking", "time": 7}
        ]
    },

    "malabar_fish_curry": {
        "name": "Malabar Fish Curry", 
        "cuisine_type": "Kerala",
        "preparation_time": 50,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "A spicy red fish curry from Malabar region made with kudampuli (kokum)",
        "ingredients": [
            {"name": "seer fish or kingfish", "quantity": 500, "unit": "grams"},
            {"name": "kudampuli", "quantity": 2, "unit": "pieces"},
            {"name": "shallots", "quantity": 10, "unit": "pieces"},
            {"name": "tomato", "quantity": 2, "unit": "medium"},
            {"name": "ginger", "quantity": 2, "unit": "inches"},
            {"name": "garlic", "quantity": 8, "unit": "cloves"},
            {"name": "red chilies", "quantity": 6, "unit": "pieces"},
            {"name": "coriander powder", "quantity": 2, "unit": "tablespoons"},
            {"name": "turmeric powder", "quantity": 0.5, "unit": "teaspoon"},
            {"name": "fenugreek seeds", "quantity": 0.25, "unit": "teaspoon"},
            {"name": "curry leaves", "quantity": 2, "unit": "sprigs"}
        ],
        "steps": [
            {"step": "Soak kudampuli in warm water", "time": 15},
            {"step": "Make spice paste with shallots, tomatoes and spices", "time": 10},
            {"step": "Cook spice paste until oil separates", "time": 10},
            {"step": "Add kudampuli water and bring to boil", "time": 5},
            {"step": "Add fish pieces and simmer until cooked", "time": 10}
        ]
    },

    # Add new chicken recipes
    "classic_butter_chicken": {
        "name": "Classic Butter Chicken",
        "cuisine_type": "North Indian",
        "preparation_time": 45,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Rich and creamy butter chicken made in authentic style with tandoor-cooked chicken in a tomato-based gravy",
        "ingredients": [
            {"name": "chicken thighs", "quantity": 800, "unit": "grams"},
            {"name": "yogurt", "quantity": 1, "unit": "cup"},
            {"name": "butter", "quantity": 100, "unit": "grams"},
            {"name": "heavy cream", "quantity": 200, "unit": "ml"},
            {"name": "tomato puree", "quantity": 400, "unit": "ml"},
            {"name": "kasuri methi", "quantity": 2, "unit": "tablespoons"},
            {"name": "ginger paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "garlic paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "garam masala", "quantity": 2, "unit": "teaspoons"},
            {"name": "red chili powder", "quantity": 1, "unit": "teaspoon"},
            {"name": "honey", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Marinate chicken in yogurt and spices", "time": 120},
            {"step": "Grill or bake chicken until charred", "time": 25},
            {"step": "Prepare makhani gravy", "time": 20},
            {"step": "Simmer chicken in gravy", "time": 15}
        ]
    },

    "chicken_tikka_masala": {
        "name": "Chicken Tikka Masala",
        "cuisine_type": "Anglo-Indian",
        "preparation_time": 50,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Grilled marinated chicken in a rich, spiced tomato-cream sauce",
        "ingredients": [
            {"name": "chicken breast", "quantity": 750, "unit": "grams"},
            {"name": "yogurt", "quantity": 1, "unit": "cup"},
            {"name": "cream", "quantity": 200, "unit": "ml"},
            {"name": "tomato sauce", "quantity": 400, "unit": "ml"},
            {"name": "onion", "quantity": 2, "unit": "large"},
            {"name": "ginger paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "garlic paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "tikka masala spice mix", "quantity": 3, "unit": "tablespoons"},
            {"name": "butter", "quantity": 50, "unit": "grams"}
        ],
        "steps": [
            {"step": "Marinate chicken in spiced yogurt", "time": 120},
            {"step": "Grill chicken tikka pieces", "time": 20},
            {"step": "Prepare masala gravy", "time": 25},
            {"step": "Combine and simmer", "time": 15}
        ]
    },

    "chicken_chettinad": {
        "name": "Chicken Chettinad",
        "cuisine_type": "South Indian",
        "preparation_time": 55,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Spicy and aromatic chicken curry from Tamil Nadu with freshly ground spices",
        "ingredients": [
            {"name": "chicken", "quantity": 750, "unit": "grams"},
            {"name": "onion", "quantity": 2, "unit": "large"},
            {"name": "tomatoes", "quantity": 3, "unit": "medium"},
            {"name": "curry leaves", "quantity": 20, "unit": "leaves"},
            {"name": "black peppercorns", "quantity": 2, "unit": "tablespoons"},
            {"name": "coriander seeds", "quantity": 3, "unit": "tablespoons"},
            {"name": "dried red chilies", "quantity": 5, "unit": "pieces"},
            {"name": "coconut", "quantity": 1, "unit": "cup"},
            {"name": "fennel seeds", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Dry roast and grind spices", "time": 15},
            {"step": "Marinate chicken", "time": 30},
            {"step": "Cook with onion-tomato base", "time": 25},
            {"step": "Simmer until done", "time": 20}
        ]
    },

    "continental_roast_chicken": {
        "name": "Continental Roast Chicken",
        "cuisine_type": "Continental",
        "preparation_time": 90,
        "difficulty_level": "Medium",
        "serving_size": 6,
        "description": "Classic herb-roasted whole chicken with crispy skin and juicy meat",
        "ingredients": [
            {"name": "whole chicken", "quantity": 1.5, "unit": "kg"},
            {"name": "butter", "quantity": 100, "unit": "grams"},
            {"name": "rosemary", "quantity": 4, "unit": "sprigs"},
            {"name": "thyme", "quantity": 4, "unit": "sprigs"},
            {"name": "garlic", "quantity": 1, "unit": "head"},
            {"name": "lemon", "quantity": 1, "unit": "whole"},
            {"name": "olive oil", "quantity": 3, "unit": "tablespoons"},
            {"name": "black pepper", "quantity": 1, "unit": "tablespoon"},
            {"name": "sea salt", "quantity": 2, "unit": "tablespoons"}
        ],
        "steps": [
            {"step": "Prepare herb butter mixture", "time": 10},
            {"step": "Season chicken inside and out", "time": 15},
            {"step": "Roast at high temperature", "time": 20},
            {"step": "Reduce heat and cook until done", "time": 45}
        ]
    },

    "chicken_cacciatore": {
        "name": "Chicken Cacciatore",
        "cuisine_type": "Italian",
        "preparation_time": 60,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Italian hunter-style chicken braised with herbs, wine, tomatoes and vegetables",
        "ingredients": [
            {"name": "chicken pieces", "quantity": 1, "unit": "kg"},
            {"name": "bell peppers", "quantity": 2, "unit": "large"},
            {"name": "mushrooms", "quantity": 200, "unit": "grams"},
            {"name": "onions", "quantity": 2, "unit": "medium"},
            {"name": "garlic", "quantity": 4, "unit": "cloves"},
            {"name": "red wine", "quantity": 200, "unit": "ml"},
            {"name": "crushed tomatoes", "quantity": 400, "unit": "grams"},
            {"name": "fresh herbs", "quantity": 1, "unit": "bunch"},
            {"name": "olive oil", "quantity": 4, "unit": "tablespoons"}
        ],
        "steps": [
            {"step": "Brown chicken pieces", "time": 15},
            {"step": "Saute vegetables", "time": 10},
            {"step": "Add wine and reduce", "time": 10},
            {"step": "Simmer with tomatoes and herbs", "time": 25}
        ]
    },

    # Add more regional chicken recipes
    "chicken_kolhapuri": {
        "name": "Chicken Kolhapuri",
        "cuisine_type": "Maharashtrian",
        "preparation_time": 60,
        "difficulty_level": "Hard",
        "serving_size": 4,
        "description": "Fiery hot chicken curry from Kolhapur region with freshly ground spices",
        "ingredients": [
            {"name": "chicken", "quantity": 800, "unit": "grams"},
            {"name": "onions", "quantity": 3, "unit": "large"},
            {"name": "grated coconut", "quantity": 1, "unit": "cup"},
            {"name": "red chilies", "quantity": 8, "unit": "pieces"},
            {"name": "garlic", "quantity": 8, "unit": "cloves"},
            {"name": "ginger", "quantity": 2, "unit": "inches"},
            {"name": "coriander seeds", "quantity": 2, "unit": "tablespoons"},
            {"name": "sesame seeds", "quantity": 2, "unit": "tablespoons"},
            {"name": "poppy seeds", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Roast and grind spices with coconut", "time": 20},
            {"step": "Prepare onion-tomato base", "time": 15},
            {"step": "Cook chicken with masala", "time": 25},
            {"step": "Finish with tempering", "time": 5}
        ]
    },

    "chicken_65": {
        "name": "Chicken 65",
        "cuisine_type": "South Indian",
        "preparation_time": 40,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Spicy deep-fried chicken with curry leaves and red chilies",
        "ingredients": [
            {"name": "boneless chicken", "quantity": 500, "unit": "grams"},
            {"name": "yogurt", "quantity": 0.5, "unit": "cup"},
            {"name": "ginger paste", "quantity": 1, "unit": "tablespoon"},
            {"name": "garlic paste", "quantity": 1, "unit": "tablespoon"},
            {"name": "red chili powder", "quantity": 2, "unit": "tablespoons"},
            {"name": "curry leaves", "quantity": 20, "unit": "pieces"},
            {"name": "corn flour", "quantity": 0.25, "unit": "cup"},
            {"name": "egg", "quantity": 1, "unit": "piece"}
        ],
        "steps": [
            {"step": "Marinate chicken", "time": 60},
            {"step": "Coat with spiced flour", "time": 10},
            {"step": "Deep fry until crispy", "time": 15},
            {"step": "Temper with curry leaves", "time": 5}
        ]
    },

    "chicken_rezala": {
        "name": "Chicken Rezala",
        "cuisine_type": "Bengali-Mughlai",
        "preparation_time": 50,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Light, aromatic chicken curry with yogurt and cashew paste",
        "ingredients": [
            {"name": "chicken", "quantity": 750, "unit": "grams"},
            {"name": "yogurt", "quantity": 1, "unit": "cup"},
            {"name": "cashew paste", "quantity": 0.25, "unit": "cup"},
            {"name": "poppy seed paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "green chilies", "quantity": 4, "unit": "pieces"},
            {"name": "cardamom", "quantity": 4, "unit": "pieces"},
            {"name": "kewra water", "quantity": 1, "unit": "teaspoon"},
            {"name": "white pepper", "quantity": 1, "unit": "teaspoon"}
        ],
        "steps": [
            {"step": "Marinate chicken in yogurt", "time": 30},
            {"step": "Prepare white gravy base", "time": 15},
            {"step": "Cook chicken in gravy", "time": 20},
            {"step": "Finish with kewra water", "time": 5}
        ]
    },

    "coq_au_vin": {
        "name": "Coq au Vin",
        "cuisine_type": "French",
        "preparation_time": 120,
        "difficulty_level": "Hard",
        "serving_size": 6,
        "description": "Classic French braised chicken in red wine with mushrooms and pearl onions",
        "ingredients": [
            {"name": "whole chicken", "quantity": 1.5, "unit": "kg"},
            {"name": "red wine", "quantity": 750, "unit": "ml"},
            {"name": "bacon lardons", "quantity": 200, "unit": "grams"},
            {"name": "pearl onions", "quantity": 20, "unit": "pieces"},
            {"name": "mushrooms", "quantity": 300, "unit": "grams"},
            {"name": "carrots", "quantity": 3, "unit": "large"},
            {"name": "thyme", "quantity": 4, "unit": "sprigs"},
            {"name": "bay leaves", "quantity": 2, "unit": "pieces"}
        ],
        "steps": [
            {"step": "Marinate chicken in wine", "time": 240},
            {"step": "Cook bacon and vegetables", "time": 20},
            {"step": "Brown chicken pieces", "time": 15},
            {"step": "Braise in wine sauce", "time": 60}
        ]
    },

    # Add final set of chicken recipes
    "chicken_schnitzel": {
        "name": "Chicken Schnitzel",
        "cuisine_type": "Austrian-Continental",
        "preparation_time": 40,
        "difficulty_level": "Easy",
        "serving_size": 4,
        "description": "Crispy breaded chicken cutlets served with lemon wedges",
        "ingredients": [
            {"name": "chicken breast", "quantity": 600, "unit": "grams"},
            {"name": "breadcrumbs", "quantity": 2, "unit": "cups"},
            {"name": "flour", "quantity": 1, "unit": "cup"},
            {"name": "eggs", "quantity": 2, "unit": "pieces"},
            {"name": "lemon", "quantity": 1, "unit": "whole"},
            {"name": "parsley", "quantity": 0.25, "unit": "cup"},
            {"name": "butter", "quantity": 50, "unit": "grams"},
            {"name": "oil", "quantity": 2, "unit": "cups"}
        ],
        "steps": [
            {"step": "Pound chicken breasts thin", "time": 10},
            {"step": "Prepare breading station", "time": 5},
            {"step": "Coat chicken pieces", "time": 10},
            {"step": "Pan fry until golden", "time": 15}
        ]
    },

    "chicken_tandoori": {
        "name": "Tandoori Chicken",
        "cuisine_type": "North Indian",
        "preparation_time": 480,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Classic tandoor-cooked chicken marinated in yogurt and spices",
        "ingredients": [
            {"name": "chicken legs", "quantity": 8, "unit": "pieces"},
            {"name": "yogurt", "quantity": 2, "unit": "cups"},
            {"name": "tandoori masala", "quantity": 3, "unit": "tablespoons"},
            {"name": "ginger paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "garlic paste", "quantity": 2, "unit": "tablespoons"},
            {"name": "lemon juice", "quantity": 2, "unit": "tablespoons"},
            {"name": "mustard oil", "quantity": 3, "unit": "tablespoons"},
            {"name": "kasoori methi", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Make deep cuts in chicken", "time": 10},
            {"step": "Prepare spiced marinade", "time": 15},
            {"step": "Marinate overnight", "time": 420},
            {"step": "Cook in tandoor/oven", "time": 35}
        ]
    },

    "kung_pao_chicken": {
        "name": "Kung Pao Chicken",
        "cuisine_type": "Chinese",
        "preparation_time": 30,
        "difficulty_level": "Medium",
        "serving_size": 4,
        "description": "Spicy stir-fried chicken with peanuts and vegetables",
        "ingredients": [
            {"name": "chicken thighs", "quantity": 600, "unit": "grams"},
            {"name": "peanuts", "quantity": 1, "unit": "cup"},
            {"name": "dried red chilies", "quantity": 8, "unit": "pieces"},
            {"name": "scallions", "quantity": 6, "unit": "stalks"},
            {"name": "soy sauce", "quantity": 3, "unit": "tablespoons"},
            {"name": "hoisin sauce", "quantity": 2, "unit": "tablespoons"},
            {"name": "rice vinegar", "quantity": 2, "unit": "tablespoons"},
            {"name": "sesame oil", "quantity": 1, "unit": "tablespoon"}
        ],
        "steps": [
            {"step": "Marinate chicken", "time": 15},
            {"step": "Roast peanuts", "time": 5},
            {"step": "Prepare sauce", "time": 5},
            {"step": "Stir-fry and combine", "time": 10}
        ]
    }
}

# Regional categorization
REGIONAL_CUISINES = {
    "North Indian": ["butter_chicken", "dal_makhani", "sarson_ka_saag", "classic_butter_chicken", "chicken_tandoori"],
    "South Indian": ["masala_dosa", "kerala_fish_curry", "chicken_chettinad", "chicken_65"],
    "Gujarati": ["dhokla"],
    "Bengali": ["fish_curry"],
    "Maharashtrian": ["vada_pav", "chicken_kolhapuri"],
    "Rajasthani": ["dal_baati"],
    "Kerala": ["kerala_fish_curry"],
    "Punjabi": ["sarson_ka_saag"],
    "Street Food": ["pani_puri"],
    "Continental": ["continental_roast_chicken", "coq_au_vin"],
    "Chinese": ["kung_pao_chicken"],
    "Italian": ["chicken_cacciatore"]
}

# Dietary categorization
DIETARY_CATEGORIES = {
    "Vegetarian": ["dal_makhani", "masala_dosa", "dhokla", "vada_pav", "dal_baati", "sarson_ka_saag", "pani_puri"],
    "Non-Vegetarian": ["butter_chicken", "fish_curry", "kerala_fish_curry", "classic_butter_chicken", "chicken_tikka_masala", "chicken_chettinad", "continental_roast_chicken", "chicken_cacciatore", "chicken_kolhapuri", "chicken_65", "chicken_rezala", "coq_au_vin"]
}

# Difficulty levels
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard", "Expert"]

# Add cooking methods for better recipe organization
COOKING_METHODS = {
    "Curry": ["butter_chicken", "chicken_tikka_masala", "chicken_chettinad", "chicken_kolhapuri", "chicken_rezala", "kerala_fish_curry", "fish_curry"],
    "Grilled": ["chicken_tandoori", "chicken_tikka"],
    "Deep Fried": ["chicken_65"],
    "Roasted": ["continental_roast_chicken"],
    "Braised": ["coq_au_vin", "chicken_cacciatore"],
    "Pan Fried": ["chicken_schnitzel"],
    "Stir Fried": ["kung_pao_chicken"]
}

# Add dietary restrictions and allergen information
DIETARY_RESTRICTIONS = {
    "Contains Dairy": ["butter_chicken", "chicken_tikka_masala", "chicken_rezala", "continental_roast_chicken"],
    "Contains Nuts": ["kung_pao_chicken", "chicken_rezala"],
    "Gluten Free": ["chicken_chettinad", "chicken_kolhapuri", "kerala_fish_curry"],
    "Egg Free": ["butter_chicken", "chicken_tikka_masala", "chicken_chettinad"],
    "Contains Alcohol": ["coq_au_vin", "chicken_cacciatore"]
}

# Add spice levels for better recipe filtering
SPICE_LEVELS = {
    "Mild": ["continental_roast_chicken", "chicken_schnitzel", "coq_au_vin", "chicken_cacciatore"],
    "Medium": ["butter_chicken", "chicken_tikka_masala", "chicken_rezala", "chicken_tandoori"],
    "Spicy": ["chicken_chettinad", "chicken_65", "chicken_kolhapuri", "kung_pao_chicken"]
}

# Recipe name variations and common alternative names
RECIPE_VARIATIONS = {
    "butter_chicken": ["butter chicken", "murgh makhani", "murg makhani"],
    "dal_makhani": ["dal makhani", "daal makhani", "black dal", "kaali dal"],
    "masala_dosa": ["masala dosa", "masale dose", "mysore masala dosa"],
    "dhokla": ["dhokla", "khaman dhokla", "khaman"],
    "fish_curry": ["fish curry", "bengali fish curry", "machher jhol", "macher jhol"],
    "vada_pav": ["vada pav", "wada pav", "vada pao", "batata vada"],
    "dal_baati": ["dal baati", "dal bati", "daal baati"],
    "kerala_fish_curry": ["kerala fish curry", "meen curry", "fish molee", "meen molee"],
    "sarson_ka_saag": ["sarson ka saag", "sarson da saag", "mustard greens"],
    "pani_puri": ["pani puri", "gol gappe", "golgappa", "puchka", "gupchup"],
    "classic_butter_chicken": ["butter chicken", "murgh makhani", "chicken makhani"],
    "chicken_tikka_masala": ["tikka masala", "CTM", "chicken tikka gravy"],
    "chicken_chettinad": ["chettinad chicken", "chettinad kozhi"],
    "chicken_kolhapuri": ["kolhapuri chicken", "tambda rassa"],
    "chicken_65": ["chicken 65", "chennai chicken 65"],
    "chicken_rezala": ["rezala", "mughlai chicken"],
    "chicken_tandoori": ["tandoori chicken", "tandoori murgh", "murgh tandoori"],
    "kung_pao_chicken": ["kung pao", "gong bao chicken"]
}

def similar(str1, str2, threshold=0.6):
    """Enhanced string similarity check with better handling of variations"""
    if not str1 or not str2:
        return False
        
    str1 = str1.lower().strip()
    str2 = str2.lower().strip()
    
    # Check for exact match or containment
    if str1 == str2 or str1 in str2 or str2 in str1:
        return True
        
    # Handle hyphenated words and special characters
    str1_clean = ''.join(e.lower() for e in str1 if e.isalnum())
    str2_clean = ''.join(e.lower() for e in str2 if e.isalnum())
    
    if str1_clean == str2_clean:
        return True
        
    # Use SequenceMatcher for fuzzy matching
    return SequenceMatcher(None, str1_clean, str2_clean).ratio() > threshold

def get_recipe_by_name(name):
    """Enhanced recipe retrieval with better error handling"""
    if not name:
        return None
        
    name = name.lower().strip()
    
    # Direct match attempt
    for recipe_id, recipe in INDIAN_RECIPES.items():
        if recipe["name"].lower() == name:
            return recipe
            
    # Check variations
    for recipe_id, variations in RECIPE_VARIATIONS.items():
        if any(similar(var, name) for var in variations):
            return INDIAN_RECIPES.get(recipe_id)
            
    # Fuzzy matching
    best_match = None
    best_ratio = 0
    
    for recipe_id, recipe in INDIAN_RECIPES.items():
        # Check main recipe name
        ratio = SequenceMatcher(None, name, recipe["name"].lower()).ratio()
        if ratio > 0.6 and ratio > best_ratio:
            best_match = recipe
            best_ratio = ratio
            
        # Check variations
        for variation in RECIPE_VARIATIONS.get(recipe_id, []):
            ratio = SequenceMatcher(None, name, variation.lower()).ratio()
            if ratio > 0.6 and ratio > best_ratio:
                best_match = recipe
                best_ratio = ratio
    
    return best_match

def get_recipes_by_cuisine(cuisine_type):
    """Get all recipes of a particular cuisine type with improved matching"""
    if not cuisine_type:
        return []
        
    cuisine_type = cuisine_type.lower().strip()
    recipes = []
    
    # Try exact match first
    for recipe in INDIAN_RECIPES.values():
        if recipe["cuisine_type"].lower() == cuisine_type:
            recipes.append(recipe)
            
    # If no exact matches, try fuzzy matching
    if not recipes:
        for recipe in INDIAN_RECIPES.values():
            if similar(recipe["cuisine_type"].lower(), cuisine_type):
                recipes.append(recipe)
    
    return recipes

def get_recipes_by_diet(diet_type):
    """Get all recipes of a particular dietary category"""
    recipes = []
    for recipe_id in DIETARY_CATEGORIES.get(diet_type, []):
        if recipe_id in INDIAN_RECIPES:
            recipes.append(INDIAN_RECIPES[recipe_id])
    return recipes

def get_recipes_by_difficulty(difficulty):
    """Get all recipes of a particular difficulty level"""
    return [recipe for recipe in INDIAN_RECIPES.values() 
            if recipe["difficulty_level"] == difficulty]

def get_recipes_by_max_time(max_time):
    """Get all recipes that can be prepared within the specified time"""
    return [recipe for recipe in INDIAN_RECIPES.values() 
            if recipe["preparation_time"] <= max_time]

def get_recipes_by_ingredient(ingredient_name):
    """Get all recipes that contain a specific ingredient"""
    if not ingredient_name:
        return []
        
    ingredient_name = ingredient_name.lower().strip()
    recipes = []
    
    for recipe in INDIAN_RECIPES.values():
        for ingredient in recipe["ingredients"]:
            if similar(ingredient["name"].lower(), ingredient_name):
                recipes.append(recipe)
                break
    
    return recipes 

def get_recipes_by_spice_level(spice_level):
    """Get all recipes of a particular spice level"""
    return [recipe for recipe in INDIAN_RECIPES.values() 
            if recipe["name"].lower() in [r.lower() for r in SPICE_LEVELS.get(spice_level, [])]]

def get_recipes_by_cooking_method(method):
    """Get all recipes using a particular cooking method"""
    return [recipe for recipe in INDIAN_RECIPES.values() 
            if recipe["name"].lower() in [r.lower() for r in COOKING_METHODS.get(method, [])]]

def get_recipes_by_dietary_restriction(restriction):
    """Get all recipes matching a dietary restriction"""
    return [recipe for recipe in INDIAN_RECIPES.values() 
            if recipe["name"].lower() in [r.lower() for r in DIETARY_RESTRICTIONS.get(restriction, [])]]

def get_recipe_suggestions(ingredients=None, cuisine_type=None, difficulty=None, spice_level=None, cooking_method=None):
    """Get recipe suggestions based on multiple criteria"""
    suggestions = []
    
    for recipe in INDIAN_RECIPES.values():
        matches_criteria = True
        
        if ingredients:
            recipe_ingredients = [ing["name"].lower() for ing in recipe["ingredients"]]
            if not all(ing.lower() in recipe_ingredients for ing in ingredients):
                matches_criteria = False
                
        if cuisine_type and recipe["cuisine_type"].lower() != cuisine_type.lower():
            matches_criteria = False
            
        if difficulty and recipe["difficulty_level"] != difficulty:
            matches_criteria = False
            
        if spice_level:
            recipe_name = recipe["name"].lower()
            if recipe_name not in [r.lower() for r in SPICE_LEVELS.get(spice_level, [])]:
                matches_criteria = False
                
        if cooking_method:
            recipe_name = recipe["name"].lower()
            if recipe_name not in [r.lower() for r in COOKING_METHODS.get(cooking_method, [])]:
                matches_criteria = False
                
        if matches_criteria:
            suggestions.append(recipe)
            
    return suggestions 