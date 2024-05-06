from rest_framework import serializers
from django.contrib.auth.models import User

from blog_app import models

"""
Сериализатор - преобразует сложные данные (модель в БД) в наш собственный тип данных (JSON, XML)
также есть возможность десериализовать данные обратно в модель после их использования
"""


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['pk', 'name']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Article
        fields = ['pk', 'title', 'short_description', 'full_description', 'photo', 'views', 'created_at', 'author',
                  'category']
        read_only_fields = ['views', 'created_at']

# class CategorySerializer(serializers.Serializer):
#     """
#     Для каждого поля что есть в нашей модели, мы объявляем соответствующие поля
#     в сериалайзере, поля из объекта модели будут подставляться в поля сериалайзера
#     и конвертироваться в json формат
#     """
#     # поле для id
#     # read_only - делает поле используемым только для чтения, при создании нового объекта данное поле заполнять не нужно
#     id = serializers.IntegerField(read_only=True)
#     # поле для name
#     name = serializers.CharField(max_length=150)
#
#     def create(self, validated_data):
#         # создание нового объекта
#         # validated_data - словарь с данными объекта этой модели для дальнейшего сохранения в БД
#         return models.Category.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         # обновление определенного объекта
#         # instance - объект предоставленный для обновления
#         # validated_data - данные которые нужно поставить вместо тех что были
#         instance.name = validated_data['name']
#         instance.save()
#         return instance
#
#
# class UserSerializer(serializers.Serializer):
#     username = serializers.CharField(read_only=True)
#     email = serializers.EmailField(read_only=True)
#     is_superuser = serializers.BooleanField(read_only=True)
#
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
#
#
# class ArticleSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=100)
#     short_description = serializers.CharField()
#     full_description = serializers.CharField()
#     photo = serializers.ImageField()
#     views = serializers.IntegerField(read_only=True)
#     created_at = serializers.DateTimeField(read_only=True)
#     author = UserSerializer()
#     category = CategorySerializer()
#
#     def create(self, validated_data):
#         pass
#
#     def update(self, instance, validated_data):
#         pass
