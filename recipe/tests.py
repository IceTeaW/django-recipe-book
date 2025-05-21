from django.test import TestCase, Client
from django.urls import reverse
from .models import Recipe, Category

class RecipeAppViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.category_salads = Category.objects.create(name="Салати")
        cls.category_soups = Category.objects.create(name="Супи")
        cls.category_empty = Category.objects.create(name="Без рецептів")

        for i in range(7):
            Recipe.objects.create(
                title=f"Салат {i+1}",
                description="Смачний салат",
                instructions="Змішати",
                ingredients="Трава",
                category=cls.category_salads
            )
        for i in range(5):
            Recipe.objects.create(
                title=f"Суп {i+1}",
                description="Гарячий суп",
                instructions="Варити",
                ingredients="Вода",
                category=cls.category_soups
            )

    def test_main_view_status_code_and_template(self):
        response = self.client.get(reverse('recipe:main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/main.html')

    def test_main_view_context_recipe_count_max_10(self):
        response = self.client.get(reverse('recipe:main'))
        self.assertTrue('recipes' in response.context)
        self.assertLessEqual(len(response.context['recipes']), 10)

    def test_main_view_shows_all_if_less_than_10_recipes(self):
        Recipe.objects.exclude(pk__in=list(Recipe.objects.all()[:3].values_list('pk', flat=True))).delete()
        self.assertEqual(Recipe.objects.count(), 3)

        response = self.client.get(reverse('recipe:main'))
        self.assertTrue('recipes' in response.context)
        self.assertEqual(len(response.context['recipes']), 3)

    def test_category_detail_view_status_code_and_template(self):
        response = self.client.get(reverse('recipe:category_detail', args=[self.category_salads.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/category_detail.html')

    def test_category_detail_view_404_for_invalid_id(self):
        invalid_pk = Category.objects.latest('pk').pk + 99
        response = self.client.get(reverse('recipe:category_detail', args=[invalid_pk]))
        self.assertEqual(response.status_code, 404)

    def test_category_detail_view_context_data(self):
        response = self.client.get(reverse('recipe:category_detail', args=[self.category_soups.pk]))
        self.assertTrue('category' in response.context)
        self.assertTrue('recipes' in response.context)
        self.assertEqual(response.context['category'], self.category_soups)

        expected_recipes_count = Recipe.objects.filter(category=self.category_soups).count()
        self.assertEqual(len(response.context['recipes']), expected_recipes_count)
        for recipe in response.context['recipes']:
            self.assertEqual(recipe.category, self.category_soups)

    def test_category_detail_view_for_empty_category(self):
        response = self.client.get(reverse('recipe:category_detail', args=[self.category_empty.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('recipes' in response.context)
        self.assertEqual(len(response.context['recipes']), 0)
        self.assertEqual(response.context['category'], self.category_empty)