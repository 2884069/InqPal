from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from inqpal.models import Account,Comment
from inqpal.urls import urlpatterns

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

    def test_comment_trending(self):
        response = self.client.post(reverse('inqpal:trending'), {
            'post': '',
            
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter().exists())


class BaseTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')

    def test_base_used_on_all_pages(self):
        for urlpattern in urlpatterns:
            try:
                response = self.client.get(reverse(f'inqpal:{urlpattern.name}'),follow=True)
            except:
                continue
            self.assertTemplateUsed(response, 'inqpal/base.html', f'{urlpattern.name} page does not use base.html as a template')

    def test_base_redirect(self):
        response = self.client.get(reverse('inqpal:index'))
        self.assertEqual(response.status_code, 302, 'index not redirecting to either trending or pals posts')
    
    
    def test_base_title(self):
        response = self.client.get(reverse('inqpal:index'), follow=True)
        content = response.content.decode()
        self.assertIn('InqPal', content, '"InqPal" not present in header when user is not loged in')
        self.assertIn('an inquisition of paleontologists', content, '"an inquisition of paleontologists" not present in header when user is not loged in')


    def test_base_login_change(self):
        """
        Checks to see if the base header changes when a user logs in.
        """
        response = self.client.get(reverse('inqpal:index'), follow=True)
        content = response.content.decode()
        self.assertIn('<a href="/inqpal/posts/trending/">Trending</a>', content, f'Trending link not present in header when user is not loged in')
        self.assertIn('<a href="/inqpal/account/login/">Login</a>', content, 'Login link not present in header when user is not loged in')
        self.assertIn('<a href="/inqpal/account/signup/">Sign Up</a>', content, 'Sign Up link not present in header when user is not loged in')
        self.assertIn('<a href="/inqpal/posts/categories/">Categories</a>', content, 'Categories link not present in header when user is not loged in')
        

        
        self.client.login(username='testuser', password='TestPassword123')
        response = self.client.get(reverse('inqpal:index'), follow=True)
        content = response.content.decode()

        self.assertIn('<a href="/inqpal/posts/trending/">Trending</a>', content, 'trending not present in header when user is loged in')
        self.assertIn(' <a href="/inqpal/posts/pals/">Pals</a>', content, 'Pals link not present in header when user is loged in')
        self.assertIn('<a href="/inqpal/account/my_account/">Account</a>', content, 'Account link not present in header when user is loged in')
        self.assertIn('<a href="/inqpal/posts/categories/">Categories</a>', content, 'Categories link not present in header when user is loged in')
    
    def test_redirect_based_on_authentication(self):
        response = self.client.get(reverse('inqpal:index'), follow=True)
        self.assertRedirects(response, reverse('inqpal:trending'), "Logged-out user was not redirected to trending page.")

        self.client.login(username='testuser', password='TestPassword123')

        response = self.client.get(reverse('inqpal:index'), follow=True)
        self.assertRedirects(response, reverse('inqpal:pals'), "Logged-in user was not redirected to pals posts page.")