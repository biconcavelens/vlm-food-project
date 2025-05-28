from food_dataset import FoodDataset

dataset = FoodDataset()

# Dictionary of dishes with their details
dishes = {
    "pasta": {
        "actual_name": "baked pasta with cheese",
        "images": [f"images/pasta/pasta{i}.png" for i in range(1, 11)],
        "vague_title": "cheesy pasta thing",
        "full_instructions": [
            "Boil 1 pound pasta in salted water until al dente, about 8-10 minutes",
            "Meanwhile, preheat oven to 350°F",
            "In a large bowl, mix cooked pasta with 2 cups marinara sauce and 1 cup mozzarella",
            "Transfer to a 9x13 baking dish",
            "Top with remaining 1 cup mozzarella cheese",
            "Bake uncovered for 25 minutes until cheese is bubbly and golden"
        ],
        "concise_steps": [
            "Cook pasta and mix with marinara sauce and cheese",
            "Layer in baking dish with extra cheese on top",
            "Bake at 350°F until bubbly"
        ]
    },
    "pizza": {
        "actual_name": "homemade pizza",
        "images": [f"images/pizza/pizza{i}.png" for i in range(1, 11)],
        "vague_title": "italian pizza",
        "full_instructions": [
            "In a large bowl, mix 2 cups flour, 1 tsp salt, 1 tsp sugar, 1 tsp dry yeast, ¾ cup warm water, and 1 tbsp olive oil",
            "Knead the dough until smooth, then let rise for 1 hour until doubled",
            "Preheat oven to 475°F and prepare a pizza stone or baking tray",
            "Roll out the dough into a 12-inch circle on a floured surface",
            "Spread ½ cup pizza sauce evenly on the dough",
            "Top with 1½ cups shredded mozzarella and any toppings of your choice",
            "Bake for 10–12 minutes until crust is golden and cheese is bubbling"
        ],
        "concise_steps": [
            "Make and rise pizza dough",
            "Roll out dough and add sauce, cheese, and toppings",
            "Bake at 475°F until crust is golden and cheese bubbles"
        ]
    },
    "chole_bature": {
        "actual_name": "chole bature",
        "images": [f"images/chole_bature/chole_bature{i}.png" for i in range(1, 11)],
        "vague_title": "spicy chickpeas with fluffy balloons",
        "full_instructions": [
            "Soak 1 cup dried chickpeas overnight, then pressure cook with salt until soft",
            "In a pan, heat oil and sauté chopped onions, ginger, and garlic until golden",
            "Add chopped tomatoes and cook until soft, then stir in spices: cumin, coriander, turmeric, garam masala, and chili powder",
            "Mix in the cooked chickpeas and simmer for 15–20 minutes, mashing some for thickness",
            "For bature: mix 2 cups all-purpose flour, 2 tbsp yogurt, ½ tsp baking powder, and water to form a soft dough",
            "Rest dough for 1 hour, then divide and roll into circles",
            "Deep fry each batura in hot oil until puffed and golden"
        ],
        "concise_steps": [
            "Cook soaked chickpeas with spiced onion-tomato masala",
            "Make and rest dough for bature",
            "Roll and deep-fry bature until puffed"
        ]
    },
    "tacos": {
        "actual_name": "meat tacos",
        "images": [f"images/tacos/tacos{i}.png" for i in range(1, 11)],
        "vague_title": "mexican folded crunchy flavor holders",
        "full_instructions": [
            "In a skillet, cook 1 lb ground meat over medium heat until browned",
            "Drain excess fat, then add 1 packet taco seasoning and ½ cup water",
            "Simmer for 5–7 minutes until thickened",
            "Warm taco shells in the oven at 350°F for 5 minutes or until crisp",
            "Spoon meat mixture into taco shells",
            "Top with shredded lettuce, diced tomatoes, cheese, and sour cream as desired"
        ],
        "concise_steps": [
            "Cook meat with taco seasoning",
            "Warm taco shells",
            "Fill with meat and toppings"
        ]
    },
    "burger": {
        "actual_name": "classic cheeseburger",
        "images": [f"images/burger/burger{i}.png" for i in range(1, 11)],
        "vague_title": "stacked meaty sandwich thing",
        "full_instructions": [
            "In a bowl, mix 1 lb ground beef with salt and pepper",
            "Form into 4 equal patties",
            "Cook patties on a hot skillet or grill for 3–4 minutes per side, or until desired doneness",
            "Toast burger buns lightly on the skillet or grill",
            "Place cooked patties on the bottom buns",
            "Add toppings like lettuce, tomato, onion, cheese, pickles, and sauces",
            "Close with top buns and serve hot"
        ],
        "concise_steps": [
            "Shape and cook beef patties",
            "Toast buns and assemble with toppings",
            "Serve warm"
        ]
    },
    "sushi": {
        "actual_name": "sushi rolls",
        "images": [f"images/sushi/sushi{i}.png" for i in range(1, 11)],
        "vague_title": "rolled rice and fish",
        "full_instructions": [
            "Cook 2 cups sushi rice according to package instructions, then let cool",
            "Mix rice vinegar, sugar, and salt, then fold into cooled rice",
            "Place a bamboo mat on a flat surface and lay a sheet of nori on it",
            "Spread a thin layer of sushi rice over the nori, leaving 1 inch at the top edge",
            "Add fillings like sliced cucumber, avocado, and raw fish along the bottom edge",
            "Using the mat, roll the sushi tightly away from you, sealing the edge with a little water",
            "Slice into bite-sized pieces with a sharp knife"
        ],
        "concise_steps": [
            "Cook and season sushi rice",
            "Spread rice on nori, add fillings, and roll tightly",
            "Slice into pieces"
        ]
    },
    "salad": {
        "actual_name": "mixed vegetable salad",
        "images": [f"images/salad/salad{i}.png" for i in range(1, 11)],
        "vague_title": "fresh crunchy vegetable mix",
        "full_instructions": [
            "Wash and chop 2 cups mixed greens (lettuce, spinach, arugula)",
            "Dice 1 cucumber, 1 bell pepper, and 1 tomato",
            "Slice ½ red onion thinly",
            "In a large bowl, combine all vegetables",
            "Drizzle with olive oil and balsamic vinegar",
            "Season with salt and pepper to taste",
            "Toss gently to combine and serve immediately"
        ],
        "concise_steps": [
            "Chop mixed greens and vegetables",
            "Combine in a bowl with dressing",
            "Toss and serve"
        ]
    },
    "curry": {
        "actual_name": "chicken curry",
        "images": [f"images/curry/curry{i}.png" for i in range(1, 11)],
        "vague_title": "spicy sauce with meat and veggies",
        "full_instructions": [
            "In a large pot, heat 2 tbsp oil over medium heat",
            "Add 1 chopped onion and sauté until golden brown",
            "Stir in 2 cloves minced garlic and 1 inch grated ginger, cooking for 1 minute",
            "Add 1 lb diced chicken or beef and cook until browned",
            "Mix in 2 tbsp curry powder, 1 tsp cumin, and salt to taste",
            "Pour in 1 can coconut milk and simmer for 20 minutes",
            "Add 2 cups chopped vegetables (potatoes, carrots, peas) and cook until tender",
            "Serve hot with rice or naan"
        ],
        "concise_steps": [
            "Sauté onion, garlic, and ginger in oil",
            "Brown meat, add spices and coconut milk",
            "Simmer with vegetables until tender, serve with rice or naan"
        ]
    },
    "omelette": {
        "actual_name": "cheese omelette",
        "images": [f"images/omelette/omelette{i}.png" for i in range(1, 11)],
        "vague_title": "fluffy egg pancake with fillings",
        "full_instructions": [
            "In a bowl, whisk 4 eggs with salt and pepper",
            "Heat 1 tbsp butter in a non-stick skillet over medium heat",
            "Pour in the eggs and cook until edges start to set, about 2 minutes",
            "Add fillings like cheese, diced vegetables, or cooked meat on one half of the omelette",
            "Fold the other half over the fillings and cook for another minute until cheese melts",
            "Slide onto a plate and serve hot"
        ],
        "concise_steps": [
            "Whisk eggs and cook in butter until edges set",
            "Add fillings, fold, and cook until cheese melts",
            "Serve hot"
        ]
    },
    "soup": {
        "actual_name": "vegetable soup",
        "images": [f"images/soup/soup{i}.png" for i in range(1, 11)],
        "vague_title": "warm liquid comfort food",
        "full_instructions": [
            "In a large pot, heat 2 tbsp oil over medium heat",
            "Add 1 chopped onion and sauté until translucent",
            "Stir in 2 cloves minced garlic and cook for 1 minute",
            "Add 4 cups vegetable or chicken broth and bring to a boil",
            "Add 2 cups diced vegetables (carrots, potatoes, celery) and simmer for 15 minutes",
            "Season with salt, pepper, and herbs like thyme or parsley",
            "Serve hot with bread"
        ],
        "concise_steps": [
            "Sauté onion and garlic in oil",
            "Add broth and vegetables, simmer until tender",
            "Season and serve hot"
        ]
    }
}

# Add all dishes to the dataset
for dish_data in dishes.values():
    dataset.add_sample(
        actual_name=dish_data["actual_name"],
        image_paths=dish_data["images"],
        vague_title=dish_data["vague_title"],
        full_instructions=dish_data["full_instructions"],
        concise_steps=dish_data["concise_steps"]
    )

dataset.save_dataset()