from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog_app.models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def root(request):
    return Response('server is running')


@api_view(['GET', 'POST'])
def read_categories(request):
    """
    Получаем JSON всех категорий из БД.
    Создаем новый объект модели категории
    """
    if request.method == 'GET':  # проверяем что отправляется GET запрос для получения данных
        # получаем queryset всех категорий
        categories = Category.objects.all()
        # отдаем queryset для сериализации, преобразованию полей из модели в json формат
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':  # при отправке POST запроса для создания
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # проверяем что введенные данные являются валидными
        serializer.save()  # вызывается метод .create() - для создания нового объекта в модели
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
def read_category(request, category_id):
    """
    Получаем данные определенной категории и сериализуем её.
    Обновляем определенный объект в БД
    """

    category = Category.objects.filter(pk=category_id)
    if not category.exists():
        return Response({'error': 'Category with this id not found'},
                        status=status.HTTP_404_NOT_FOUND)

    category = category.first()
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)