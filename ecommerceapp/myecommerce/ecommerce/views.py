from django.contrib.auth import authenticate
from rest_framework import generics, permissions, status, parsers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import update_last_login
from rest_framework.views import APIView
from .models import User, Store, Product, Review, Order, OrderItem, Category, Profile
from .paginators import CoursePaginator
from .serializers import UserSerializer, ProfileSerializer, StoreSerializer, ProductSerializer, ReviewSerializer, \
    OrderSerializer, OrderItemSerializer, PaymentSerializer, ShippingAddressSerializer, CategorySerializer, \
    LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({'message': 'Đăng ký tài khoản thành công'}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Đăng ký tài khoản thất bại'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None and user.is_active:
            update_last_login(None, user)
            return Response({'message': 'Đăng nhập thành công'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Tên đăng nhập hoặc mật khẩu không đúng'}, status=status.HTTP_401_UNAUTHORIZED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CoursePaginator
    permission_classes = [permissions.IsAuthenticated]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Profile.objects.filter(user=self.request.user)
        else:
            return Profile.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class StoreListCreateView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = StoreSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Store.objects.all()

    def perform_create(self, serializer):
        serializer.save()


class ProductListCreateView(viewsets.ViewSet, generics.ListCreateAPIView):
    serializer_class = ProductSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Product.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, pk=None):
        try:
            product = self.get_queryset().get(pk=pk)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['put'])
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

    @action(detail=True, methods=['patch'])
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


class ReviewListCreateView(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, product_id):
        reviews = Review.objects.filter(product_id=product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def add_item(self, request):
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
    def set_payment(self, request):
        order = self.get_object()
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
