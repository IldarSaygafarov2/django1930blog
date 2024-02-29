from django.contrib import admin
from .models import Category, Article, Comment, Like, Dislike

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created_at', 'author', 'category')
    list_display_links = ('pk', 'title')
    list_editable = ('author', 'category')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name')



class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created_at', 'author', 'article')
    list_filter = ('author', 'article')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Like)
admin.site.register(Dislike)
