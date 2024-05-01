from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog_app.models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def root(request):
    return Response('server is running')


@api_view(['GET'])
def read_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    # serializer.is_valid(raise_exception=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
