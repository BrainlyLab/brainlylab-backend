from django.urls import path
from .views import ProfileAPIView, CoinsHistoryAPIView, AddCoinsAPIView

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='profile-detail'),
    path('coins/', CoinsHistoryAPIView.as_view(), name='coins-history'),
    path('coins/add/', AddCoinsAPIView.as_view(), name='coins-add'),
]
