from django.urls import path

from . import views


urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.HomePageView.as_view(), name='home'),
    path('categories/<int:category_id>/', views.category_articles, name='category_articles'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('articles/<int:article_id>/', views.article_detail, name='detail'),
    path('create/', views.create_article, name='create'),
    path('update/<int:pk>/', views.UpdateArticle.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteArticle.as_view(), name='delete'),

    path('search/', views.SearchResults.as_view(), name='search'),
    path('authors/<int:user_id>/', views.author_page, name='author_page'),
    path('add_vote/<str:obj_type>/<int:obj_id>/<str:action>/', views.add_vote, name='add_vote')
]