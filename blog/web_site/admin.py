from django.contrib import admin
from .models import Category, Article, Comment


# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'views', 'author', 'category', 'photo_preview')
    list_display_links = ('pk', 'title')
    readonly_fields = ('views',)
    list_editable = ('author', 'category')
    list_filter = ('author', 'category')


admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
