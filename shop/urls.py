from django.urls import path, include

from rest_framework import routers

from .views import CategoryViewset, ProductView

app_name = 'shop'

# Ici nous créons notre routeur
router = routers.SimpleRouter()
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register('category', CategoryViewset, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('product/', ProductView.as_view())
    ]
