from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, Product, Article


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id', 'date_created', 'date_updated', 'name', 'price', 'product'
            ]


class ProductSerializer(ModelSerializer):

    articles = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name',
            'date_created', 'date_updated',
            'category', 'articles'
            ]

    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated']


class CategoryDetailSerializer(ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data



