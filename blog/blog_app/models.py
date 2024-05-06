from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'  # Отображение название модельки(класса) в единственном числе
        verbose_name_plural = 'Категории'  # Отображение название модельки(класса) во множественном числе
        ordering = ['pk']


class Article(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    short_description = models.TextField(max_length=150, verbose_name='Краткое описание статьи')
    full_description = models.TextField(verbose_name='Полное описание статьи')
    photo = models.ImageField(verbose_name='Фото', upload_to='photos/articles/', blank=True, null=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='articles')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'article_pk': self.pk})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name='Статья')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    body = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.article}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ArticleCountViews(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=255)


class Like(models.Model):
    user = models.ManyToManyField(User, related_name='likes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='likes', blank=True, null=True)


class Dislike(models.Model):
    user = models.ManyToManyField(User, related_name='dislikes')
    article = models.OneToOneField(Article, on_delete=models.CASCADE, related_name='dislikes', blank=True, null=True)
    comment = models.OneToOneField(Comment, on_delete=models.CASCADE, related_name='dislikes', blank=True, null=True)
