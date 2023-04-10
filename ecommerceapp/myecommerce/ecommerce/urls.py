from django.urls import include, path
from rest_framework import routers
from .views import RegisterView, LoginView, ProfileView, StoreListCreateView, ProductListCreateView, \
    ReviewListCreateView, OrderListCreateView, CategoryViewSet,UserViewSet

router = routers.DefaultRouter()
router.register(r'stores', StoreListCreateView, basename='store')
router.register(r'products', ProductListCreateView, basename='product')
router.register(r'reviews', ReviewListCreateView, basename='review')
router.register(r'orders', OrderListCreateView, basename='order')
router.register(r'users', UserViewSet, basename='user')
router.register(r'categories', CategoryViewSet, basename='category')



urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]




