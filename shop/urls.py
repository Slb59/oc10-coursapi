from django.urls import path, include

from rest_framework import routers

from .views import CategoryViewset, ProductViewset, ArtcileViewset
from .views import AdminCategoryViewset, AdminArticleViewset

app_name = 'shop'

# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('category', CategoryViewset, basename='category')
router.register('product', ProductViewset, basename='product')
router.register('article', ArtcileViewset, basename='article')
router.register(
    'admin/category', AdminCategoryViewset, basename='admin-category'
    )
router.register(
    'admin/article', AdminArticleViewset, basename='admin-article'
    )

urlpatterns = [
    path('', include(router.urls))
    ]
