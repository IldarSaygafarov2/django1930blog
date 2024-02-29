from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import mark_safe

# Create your models here.

# web_site_category

# verbose_name - альтернативное название поля в админке


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # меняет название таблицы в единственном числе
        verbose_name_plural = 'Категории'  # меняет название таблицы во множественном числе


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название статьи')
    short_description = models.TextField(max_length=150, verbose_name='Краткое описание статьи')
    full_description = models.TextField(verbose_name='Полное описание статьи')
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/articles/', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='articles')

    def __str__(self):
        return self.title

    def photo_preview(self):
        if self.photo:
            return mark_safe(f'<img src="{self.photo.url}" width="50" height="50">')

    def get_absolute_url(self):
        return reverse('detail', kwargs={'article_id': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class ArticleCountViews(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=150)


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='likes')
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislikes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='dislikes')
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, blank=True, null=True,
                                   related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)