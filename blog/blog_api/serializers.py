from rest_framework import serializers

from blog_app import models

"""
Сериализатор - преобразует сложные данные (модель в БД) в наш собственный тип данных (JSON, XML)
также есть возможность десериализовать данные обратно в модель после их использования
"""


class CategorySerializer(serializers.Serializer):
    """
    Для каждого поля что есть в нашей модели, мы объявляем соответствующие поля
    в сериалайзере, поля из объекта модели будут подставляться в поля сериалайзера
    и конвертироваться в json формат
    """
    id = serializers.IntegerField()  # поле для id
    name = serializers.CharField(max_length=150)  # поле для name

    def create(self, validated_data):
        # создание нового объекта
        # validated_data - словарь с данными объекта этой модели для дальнейшего сохранения в БД
        pass

    def update(self, instance, validated_data):
        # обновление определенного объекта
        # instance - объект предоставленный для обновления
        # validated_data - данные которые нужно поставить вместо тех что были
        pass
