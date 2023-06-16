from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, Product, Article


class ArticleListSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id', 'date_created', 'date_updated', 'name', 'product', 'price'
            ]

    def validate_price(self, value):

        if value <= 1:
            raise serializers.ValidationError('Price must be > 1')
        return value

    def validate_product(self, value):

        if value.active is False:
            raise serializers.ValidationError('Inactive product')
        return value


class ArticleDetailSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id', 'date_created', 'date_updated', 'name', 'price', 'product'
            ]


class ProductListSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id', 'name',
            'date_created', 'date_updated',
            'description',
            'category',
            'ecoscore'
            ]


class ProductDetailSerializer(ModelSerializer):

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
        serializer = ArticleListSerializer(queryset, many=True)
        return serializer.data


class CategoryListSerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'date_created', 'date_updated', 'description'
            ]

    def validate_name(self, value):

        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError('Category already exists')
        return value

    def validate(self, data):
        if data['name'] not in data['description']:
            raise serializers.ValidationError('Name must be in description')
        return data


class CategoryDetailSerializer(ModelSerializer):

    products = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'date_created', 'date_updated', 'products']

    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data
