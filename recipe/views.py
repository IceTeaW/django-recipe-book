from django.shortcuts import render
from .models import Recipe # Імпорт вашої моделі Recipe
import random

def main_view(request): # Назва view згідно завдання: main
    all_recipes_list = list(Recipe.objects.all())

    if len(all_recipes_list) >= 10:
        random_recipes = random.sample(all_recipes_list, 10)
    else:
        random_recipes = all_recipes_list

    context = {
        'recipes': random_recipes
    }
    return render(request, 'recipe/main.html', context)
