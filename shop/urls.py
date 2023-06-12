from django.urls import path

from .views import CategoryView, ProductView

app_name = 'shop'

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('product/', ProductView.as_view())
    ]
