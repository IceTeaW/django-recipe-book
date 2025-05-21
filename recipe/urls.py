from django.urls import path
from . import views

app_name = 'recipe'

urlpatterns = [
    path('', views.main_view, name='main'),
    path('category/<int:category_id>/', views.category_detail_view, name='category_detail'),
]