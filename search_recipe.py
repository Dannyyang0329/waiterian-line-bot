import random
import requests
from bs4 import BeautifulSoup

base_url = 'https://icook.tw/'
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}


dessert_info = {
    'random': {
        'url': 'https://icook.tw/categories/57',
        'page_limit': 100
    },
    'pudding': {
        'url': 'https://icook.tw/categories/345',
        'page_limit': 30
    },
    'chocolate': {
        'url': 'https://icook.tw/categories/73',
        'page_limit': 35
    },
    'cookie': {
        'url': 'https://icook.tw/categories/17',
        'page_limit': 105
    },
    'bread': {
        'url': 'https://icook.tw/categories/15',
        'page_limit': 100
    }
}


dish_info ={
    'random': {
        'url': 'https://icook.tw/categories/608',
        'page_limit': 100
    },
    'beef': {
        'url': 'https://icook.tw/categories/39',
        'page_limit': 100
    },
    'pork': {
        'url': 'https://icook.tw/categories/40',
        'page_limit': 100
    },
    'chicken': {
        'url': 'https://icook.tw/categories/38',
        'page_limit': 100
    },
    'seafood': {
        'url': 'https://icook.tw/categories/3',
        'page_limit': 100
    },
    'egg': {
        'url': 'https://icook.tw/categories/301',
        'page_limit': 100
    },
    'vegetable': {
        'url': 'https://icook.tw/categories/394',
        'page_limit': 100
    }
}
exotic_info = {
    'japanese': {
        'url': 'https://icook.tw/categories/60',
        'page_limit': 70
    },
    'american': {
        'url': 'https://icook.tw/categories/590',
        'page_limit': 13
    },
    'korean': {
        'url': 'https://icook.tw/categories/61',
        'page_limit': 80
    },
    'italian': {
        'url': 'https://icook.tw/categories/63',
        'page_limit': 100
    },
    'thai': {
        'url': 'https://icook.tw/categories/62',
        'page_limit': 55
    },
}
drink_info = {
    'ice': {
        'url': 'https://icook.tw/categories/20',
        'page_limit': 35
    },
    'drink': {
        'url': 'https://icook.tw/categories/463',
        'page_limit': 40
    },
    'toppings': {
        'url': 'https://icook.tw/categories/599',
        'page_limit': 21
    },
}


def get_infomation(type, category):
    if type == 'dessert':
        if category == 'random':
            return dessert_info['random']['url'], dessert_info['random']['page_limit']
        elif category == 'pudding':
            return dessert_info['pudding']['url'], dessert_info['pudding']['page_limit']
        elif category == 'chocolate':
            return dessert_info['chocolate']['url'], dessert_info['chocolate']['page_limit']
        elif category == 'cookie':
            return dessert_info['cookie']['url'], dessert_info['cookie']['page_limit']
        elif category == 'bread':
            return dessert_info['bread']['url'], dessert_info['bread']['page_limit']
    elif type == 'dish':
        if category == 'random':
            return dish_info['random']['url'], dish_info['random']['page_limit']
        elif category == 'beef':
            return dish_info['beef']['url'], dish_info['beef']['page_limit']
        elif category == 'pork':
            return dish_info['pork']['url'], dish_info['pork']['page_limit']
        elif category == 'chicken':
            return dish_info['chicken']['url'], dish_info['chicken']['page_limit']
        elif category == 'seafood':
            return dish_info['seafood']['url'], dish_info['seafood']['page_limit']
        elif category == 'egg':
            return dish_info['egg']['url'], dish_info['egg']['page_limit']
        elif category == 'vegetable':
            return dish_info['vegetable']['url'], dish_info['vegetable']['page_limit']
    elif type == 'exotic':
        if category == 'japanese':
            return exotic_info['japanese']['url'], exotic_info['japanese']['page_limit']
        elif category == 'american':
            return exotic_info['american']['url'], exotic_info['american']['page_limit']
        elif category == 'korean':
            return exotic_info['korean']['url'], exotic_info['korean']['page_limit']
        elif category == 'italian':
            return exotic_info['italian']['url'], exotic_info['italian']['page_limit']
        elif category == 'thai':
            return exotic_info['thai']['url'], exotic_info['thai']['page_limit']
    elif type == 'drink':
        if category == 'toppings':
            return drink_info['toppings']['url'], drink_info['toppings']['page_limit']
        elif category == 'drink':
            return drink_info['drink']['url'], drink_info['drink']['page_limit']
        elif category == 'ice':
            return drink_info['ice']['url'], drink_info['ice']['page_limit']
    return '', 0


def get_recipe(type, category):
    target_url, target_page_limit = get_infomation(type, category)

    selected_recipes = []
    page_idx = [random.randint(0, target_page_limit) for i in range(2)]
    page_idx = random.sample(list(range(target_page_limit)), 2)

    # get random recipes from random pages
    for random_page in page_idx:
        page_url = target_url + '?page=' + str(random_page)

        # get recipes in target page
        response = requests.get(page_url, headers=agent)
        soup = BeautifulSoup(response.text, 'html.parser')

        # pick 5 recipe
        recipes = soup.find_all("li", {"class": "browse-recipe-item"})
        recipes_num = len(recipes)
        recipe_idices = random.sample(list(range(recipes_num)), 5 if recipes_num >= 5 else recipes_num)

        for recipe_idx in recipe_idices:
            recipe = {}
            recipe.update({"name": recipes[recipe_idx].find('h2').get('data-title')})
            recipe.update({"href": "https://icook.tw" + recipes[recipe_idx].find('a').get('href')})
            recipe.update({"img_url": recipes[recipe_idx].find('img').get('data-src')})
            recipe.update({"ingredient": recipes[recipe_idx].find_all("p", {"class" : "browse-recipe-content-ingredient"})[0].text[4:-1]})
            selected_recipes.append(recipe)
    return selected_recipes


def get_search_recipe(target):
    selected_recipes = []
    target_url = "https://icook.tw/search/" + target

    # get recipes in target page
    response = requests.get(target_url, headers=agent)
    soup = BeautifulSoup(response.text, 'html.parser')

    # pick 10 recipes
    recipes = soup.find_all("li", {"class": "browse-recipe-item"})
    recipes_num = len(recipes)

    for i in range(10):
        if i < recipes_num:
            recipe = {}
            recipe.update({"name": recipes[i].find('h2').get('data-title')})
            recipe.update({"href": "https://icook.tw" + recipes[i].find('a').get('href')})
            recipe.update({"img_url": recipes[i].find('img').get('data-src')})
            recipe.update({"ingredient": recipes[i].find_all("p", {"class" : "browse-recipe-content-ingredient"})[0].text[4:-1]})
            selected_recipes.append(recipe)

    return selected_recipes

