from django.urls import include, path
from rest_framework import routers
from .views import ProductListAPIView,CategoryListAPIView,CartCreateAPIView,CartItemListCreateAPIView,OrderCreateAPIView

router = routers.DefaultRouter()
router.register(r'products', ProductListAPIView, basename='product')
router.register(r'categories', CategoryListAPIView, basename='category')
router.register(r'carts', CartCreateAPIView, basename='cart')
router.register(r'cart-items', CartItemListCreateAPIView, basename='cart-item')
router.register(r'orders', OrderCreateAPIView, basename='order')

urlpatterns = [
    path('api/', include(router.urls)),
]
