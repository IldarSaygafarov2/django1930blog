from django.urls import path

from . import views


urlpatterns = [
    path('', views.root),
    path('categories/', views.read_categories),
    path('categories/<int:category_id>/', views.read_category),
    path('articles/', views.read_articles)
]

