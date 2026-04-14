from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import RegisterView, ProfileAPIView, CoinsHistoryAPIView, AddCoinsAPIView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', ProfileAPIView.as_view(), name='profile-detail'),
    path('profile/coins/', CoinsHistoryAPIView.as_view(), name='coins-history'),
    path('profile/coins/add/', AddCoinsAPIView.as_view(), name='coins-add'),
]
