from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from blog_app.models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def root(request):
    return Response('server is running')


@api_view(['GET'])
def read_categories(request):
    """
    Получаем JSON всех категорий из БД.
    """

    # получаем queryset всех категорий
    categories = Category.objects.all()
    # отдаем queryset для сериализации, преобразованию полей из модели в json формат
    serializer = CategorySerializer(categories, many=True)
    # serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def read_category(request, category_id):
    """
    Получаем данные определенной категории и сериализуем её.
    """

    category = Category.objects.filter(pk=category_id)
    if not category.exists():
        return Response({'error': 'Category with this id not found'}, status=status.HTTP_404_NOT_FOUND)

    category = category.first()
    serializer = CategorySerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)