from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category
import random

def main_view(request):
    all_recipes_list = list(Recipe.objects.all())

    if len(all_recipes_list) >= 10:
        random_recipes = random.sample(all_recipes_list, 10)
    else:
        random_recipes = all_recipes_list

    context = {
        'recipes': random_recipes
    }
    return render(request, 'recipe/main.html', context)
def category_detail_view(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    recipes_in_category = category.categories.all()

    context = {
        'category': category,
        'recipes': recipes_in_category,
    }
    return render(request, 'recipe/category_detail.html', context)
