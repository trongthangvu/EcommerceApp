from django.urls import include, path
from rest_framework import routers
from .views import RegisterView, LoginView, ProfileView, StoreListCreateView, ProductListCreateView, ReviewListCreateView, OrderListCreateView

router = routers.SimpleRouter()
router.register(r'stores', StoreListCreateView, basename='store')
router.register(r'products', ProductListCreateView, basename='product')
router.register(r'reviews', ReviewListCreateView, basename='review')
router.register(r'orders', OrderListCreateView, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]




