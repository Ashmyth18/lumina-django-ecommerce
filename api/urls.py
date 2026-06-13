from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='api-product')
router.register('categories', views.CategoryViewSet, basename='api-category')
router.register('orders', views.OrderViewSet, basename='api-order')

urlpatterns = [
    path('', views.api_root),
    path('', include(router.urls)),
]
