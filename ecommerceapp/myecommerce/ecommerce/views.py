from rest_framework import generics, permissions, status, parsers, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login

from .backends import EcommerceBackend
from .models import User, Store, Product, Review, Order, OrderItem, Category
from .paginators import CoursePaginator
from .serializers import UserSerializer, ProfileSerializer, StoreSerializer, ProductSerializer, ReviewSerializer, \
    OrderSerializer, OrderItemSerializer, PaymentSerializer, ShippingAddressSerializer, CategorySerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    authentication_classes = [EcommerceBackend]
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = EcommerceBackend().authenticate(request, username=username, password=password)
        if user:
            update_last_login(None, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CoursePaginator
    permission_classes = [permissions.IsAuthenticated]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class StoreListCreateView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Store.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ProductListCreateView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(store__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(store__user=self.request.user)

    def destroy(self, request, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewListCreateView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        reviews = Review.objects.filter(user=user)
        products = Product.objects.filter(store__in=Store.objects.all())
        queryset = reviews.filter(product__in=products)
        return queryset

class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get', 'put'], detail=False, url_path='current-user')
    def current_user(self, request):
        u = request.user
        if request.method.__eq__('PUT'):
            for k, v in request.data.items():
                setattr(u, k, v)
            u.save()

        return Response(UserSerializer(u, context={'request': request}).data)

class OrderListCreateView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def add_item(self, request, pk=None):
        order = self.get_object()
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'])
    def update_item(self, request, pk=None):
        order = self.get_object()
        try:
            order_item = order.order_items.get(id=request.data['order_item_id'])
        except OrderItem.DoesNotExist:
            return Response({'error': 'Invalid order item ID'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = OrderItemSerializer(order_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        order = self.get_object()
        try:
            order_item = order.order_items.get(id=request.data['order_item_id'])
        except OrderItem.DoesNotExist:
            return Response({'error': 'Invalid order item ID'}, status=status.HTTP_400_BAD_REQUEST)
        order_item.delete()
        return Response({'success': True})

    @action(detail=True, methods=['post'])
    def set_shipping_address(self, request, pk=None):
        order = self.get_object()
        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def set_payment(self, request, pk=None):
        order = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)