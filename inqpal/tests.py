from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from inqpal.models import Account

class LoginAndSignUpTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')

    def test_signup_valid(self):
        response = self.client.post(reverse('inqpal:register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass123',
            'confirmation_password': 'StrongPass123',
            'fav_dino': 'Velociraptor'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Account.objects.filter(user__username='newuser').exists())

    def test_signup_password_mismatch(self):
        response = self.client.post(reverse('inqpal:register'), {
            'username': 'user8',
            'email': 'user2@example.com',
            'password': 'SomePass123',
            'confirmation_password': 'WrongPass123',
            'fav_dino': 'Stegosaurus'
        })
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, "", status_code=302)
        self.assertFalse(User.objects.filter(username='user2').exists())

    def test_login_valid(self):
        response = self.client.post(reverse('inqpal:login'), {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        self.assertEqual(response.status_code, 302)  
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_invalid(self):
        response = self.client.post(reverse('inqpal:login'), {
            'username': 'testuser',
            'password': 'WrongPassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid login details supplied.", status_code=200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='TestPassword123')
        response = self.client.get(reverse('inqpal:logout'))
        self.assertEqual(response.status_code, 302)  
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_login_empty_fields(self):
        response = self.client.post(reverse('inqpal:login'), {
            'username': '',
            'password': ''
        })
        print(response.content.decode())  

        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "", status_code=200)

    def test_login_non_existent_user(self):
        response = self.client.post(reverse('inqpal:login'), {
            'username': 'ghostUser',
            'password': 'SomePass123'
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "Invalid login details supplied.", status_code=200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_signup_weak_password(self):
        response = self.client.post(reverse('inqpal:register'), {
            'username': 'testUser2',
            'email': 'testUser2@test.com',
            'password': '1234',
            'confirmation_password': '1234',
            'fav_dino': 'Triceratops'
        })  
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "This password is too short.", status_code=200)  
        self.assertFalse(User.objects.filter(username='testUser2').exists())

    def test_signup_existing_user(self):
        User.objects.create_user(username='existingUser', email='someEmail@gmail.com', password='S0m3P@ss?')

        response = self.client.post(reverse('inqpal:register'), {
            'username': 'existingUser',
            'email': 'someEmail@gmail.com',
            'password': 'S0m3P@ss?',
            'confirmation_password': 'S0m3P@ss?',
            'fav_dino': 'Brachiosaurus'
        })

        self.assertEqual(response.status_code, 200)  
        self.assertEqual(User.objects.filter(username='existingUser').count(), 1)  
        self.assertContains(response, "A user with that username already exists.", status_code=200)

    def test_signup_missing_fields(self):
        response = self.client.post(reverse('inqpal:register'), {'username': ''})  
        self.assertEqual(response.status_code, 200)  
        self.assertFalse(User.objects.filter(username='').exists())
