from rest_framework.serializers import ModelSerializer

from shop.models import Category, Product, Article


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated']


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'date_created', 'date_updated', 'category']


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id', 'date_created', 'date_updated', 'name', 'price', 'product'
            ]
