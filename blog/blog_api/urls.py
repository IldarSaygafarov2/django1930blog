from django.urls import path

from . import views


urlpatterns = [
    path('', views.root),
    path('categories/', views.read_categories)
]

