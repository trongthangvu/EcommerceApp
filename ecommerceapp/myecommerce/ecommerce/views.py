from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import action

from .models import Category, Product, Cart, CartItem, Order
from rest_framework.response import Response
from .serializers import (
    CategorySerializer, ProductSerializer, CartSerializer,
    CartItemSerializer, OrderSerializer
)

class CategoryListAPIView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class ProductListAPIView(viewsets.ViewSet, generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class CartCreateAPIView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemListCreateAPIView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        return CartItem.objects.filter(cart_id=cart_id, cart__user=self.request.user)

    def perform_create(self, serializer):
        cart_id = self.kwargs['cart_id']
        cart = Cart.objects.get(id=cart_id, user=self.request.user)
        serializer.save(cart=cart)

class OrderCreateAPIView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart_id = self.request.data.get('cart_id')
        cart = Cart.objects.get(id=cart_id, user=self.request.user)
        serializer.save(user=self.request.user, cart=cart)
