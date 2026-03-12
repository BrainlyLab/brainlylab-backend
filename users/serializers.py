from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, BrainlyCoins

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', required=False)

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'avatar', 'brainlycoins']
        read_only_fields = ['brainlycoins']

    def validate_avatar(self, value):
        if value:
            # 500 KB limit validation
            if value.size > 500 * 1024:
                raise serializers.ValidationError("Avatar image size must be under 500KB.")
        return value


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        if 'username' in user_data:
            instance.user.username = user_data['username']
            instance.user.save()

        # Update avatar if provided
        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']

        return super().update(instance, validated_data)

class BrainlyCoinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrainlyCoins
        fields = ['id', 'coins_earned', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']
