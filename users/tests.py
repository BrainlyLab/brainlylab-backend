from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from .models import UserProfile, BrainlyCoins
import io
from PIL import Image

class UserProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_upload_small_avatar(self):
        small_image = SimpleUploadedFile(name='small.jpg', content=b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b', content_type='image/gif')
        response = self.client.patch('/api/profile/', {'avatar': small_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('/media/avatars/small', response.data['avatar'])

    def test_upload_large_avatar(self):
        gif_header_and_body = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        large_content = gif_header_and_body + (b'x' * (550 * 1024))
        large_image = SimpleUploadedFile(name='large.gif', content=large_content, content_type='image/gif')
        
        response = self.client.patch('/api/profile/', {'avatar': large_image}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('avatar', response.data)
        self.assertEqual(str(response.data['avatar'][0]), "Avatar image size must be under 500KB.")



    def test_coins_add(self):
        response = self.client.post('/api/profile/coins/add/', {'coins_earned': 50, 'reason': 'Test game'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.brainlycoins, 50)
        
        # Check history
        history = self.client.get('/api/profile/coins/')
        self.assertEqual(len(history.data), 1)
        self.assertEqual(history.data[0]['coins_earned'], 50)
