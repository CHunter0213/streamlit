import streamlit as st
import requests

URL_TAG = "url"  # Define the tag for hyperlinks

# Replace with your Edamam API credentials
app_id = 'crh40568@uga.edu'
app_key = 'ds2grouppass'

def get_extra_ingredients(recipe_ingredients, user_ingredients):
    extra_ingredients = [ingredient.lower() for ingredient in recipe_ingredients if ingredient not in user_ingredients]
    return extra_ingredients

def recommend_recipes(ingredients, preferences):
    base_url = 'https://api.edamam.com/search'
    params = {
        'q': ','.join(ingredients),
        'app_id': '92816308',
        'app_key': '23dbea385c7aad6180790ecc1758603e',
    }

    diet = preferences.get('diet', '')
    meal_type = preferences.get('mealType', '')
    health = preferences.get('health', '')

    if diet:
        params['diet'] = diet
    if meal_type:
        params['mealType'] = meal_type
    if health:
        params['health'] = health

    response = requests.get(base_url, params=params)
    data = response.json()

    if 'hits' in data:
        recipes = data['hits']

        # Create a list to store recipes along with the list of extra ingredients
        recipe_extra_ingredients = []

        for recipe in recipes:
            recipe_ingredients = [ingredient['text'].lower() for ingredient in recipe['recipe']['ingredients']]
            extra_ingredients = get_extra_ingredients(recipe_ingredients, ingredients)

            # Append the recipe along with the list of extra ingredients to the list
            recipe_extra_ingredients.append((recipe, extra_ingredients))

        # Sort the recipes based on the length of the list of extra ingredients
        sorted_recipes = sorted(recipe_extra_ingredients, key=lambda x: len(x[1]))

        # Extract only the top 5 recipes
        top_5_recipes = sorted_recipes[:5]

        result_text = ""
        for recipe, extra_ingredients in top_5_recipes:
            result_text += f"{recipe['recipe']['label']} (Extra Ingredients: {', '.join(extra_ingredients)})\n"
            result_text += recipe['recipe']['url'] + "\n" + '-' * 30 + "\n"

        return result_text

def main():
    st.title("Recipe Recommendation App")

    ingredients = st.text_input("Enter ingredients (comma-separated):")
    diet = st.text_input("Enter diet type (e.g., balanced, high-protein, low-fat):")
    meal_type = st.text_input("Enter meal type (e.g., breakfast, lunch, dinner):")
    health = st.text_input("Enter health labels (e.g., vegetarian, vegan, gluten-free):")

    preferences = {'diet': diet, 'mealType': meal_type, 'health': health}

    if st.button("Recommend Recipes"):
        result_text = recommend_recipes(ingredients.split(','), preferences)
        st.text(result_text)

        start = 1.0
        for line in result_text.split('\n'):
            if line.startswith("http"):
                st.markdown(f'<a href="{line}" target="_blank">{line}</a>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
