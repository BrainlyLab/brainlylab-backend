from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.contrib.auth.models import User
from .models import UserProfile, BrainlyCoins
from .serializers import UserProfileSerializer, BrainlyCoinsSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user.profile

class CoinsHistoryAPIView(generics.ListAPIView):
    serializer_class = BrainlyCoinsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BrainlyCoins.objects.filter(user=self.request.user).order_by('-created_at')

class AddCoinsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        coins = request.data.get('coins_earned', 0)
        reason = request.data.get('reason', 'Earned in game')
        
        try:
            coins = int(coins)
        except ValueError:
            return Response({'error': 'coins_earned must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if coins <= 0:
            return Response({'error': 'coins_earned must be positive'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            history = BrainlyCoins.objects.create(
                user=request.user,
                coins_earned=coins,
                reason=reason
            )
            # Update the total in UserProfile
            profile = request.user.profile
            profile.brainlycoins += coins
            profile.save()

        return Response(BrainlyCoinsSerializer(history).data, status=status.HTTP_201_CREATED)
