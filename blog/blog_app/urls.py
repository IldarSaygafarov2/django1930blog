from django.urls import path


from . import views


urlpatterns = [
    # path('', views.home_view, name='home'),
    path('', views.HomePageView.as_view(), name='home'),
    path('categories/<int:category_id>/', views.get_category_articles_view, name='category_articles'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration_view, name='registration'),
    path('logout/', views.user_logout, name='logout'),
    path('articles/<int:article_pk>/', views.article_detail, name='detail'),
    path('create/', views.create_article, name='create'),
    path('update/<int:pk>/', views.UpdateArticle.as_view(), name='update'),
    path('delete/<int:pk>/', views.DeleteArticle.as_view(), name='delete'),
    path('search/', views.SearchResults.as_view(), name='search'),
    path('authors/<int:user_pk>/', views.author_view, name='author'),
    path('<str:obj_type>/<int:obj_id>/<str:action>/', views.add_vote, name='add_vote')
]

# http://127.0.0.1:8000/categories/<int:category_id>/
