from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from inqpal.models import Account, Category,Comment, Post
from inqpal.urls import urlpatterns
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse, JsonResponse



from inqpal_project import settings

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
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The passwords you entered do not match.", status_code=200)
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
        self.assertIn('<a href="/inqpal/posts/pals/">Pals</a>', content, 'Pals link not present in header when user is loged in')
        self.assertIn('<a href="/inqpal/account/my_account/">Account</a>', content, 'Account link not present in header when user is loged in')
        self.assertIn('<a href="/inqpal/posts/categories/">Categories</a>', content, 'Categories link not present in header when user is loged in')
    
    def test_redirect_based_on_authentication(self):
        response = self.client.get(reverse('inqpal:index'), follow=True)
        self.assertRedirects(response, reverse('inqpal:trending'), status_code=302, msg_prefix="Logged out user was not redirected to trending page.")

        self.client.login(username='testuser', password='TestPassword123')

        response = self.client.get(reverse('inqpal:index'), follow=True)
        self.assertRedirects(response, reverse('inqpal:palsposts'), status_code=302, msg_prefix="Logged in user was not redirected to pals posts page.")



class AddPalTests(TestCase):   
    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='TestPassword123')
        self.user2 = User.objects.create_user(username='testuser2', password='TestPassword123')

        self.account1 = Account.objects.create(user=self.user1, fav_dino="T-Rex")
        self.account2 = Account.objects.create(user=self.user2, fav_dino="Velociraptor")

        self.client.login(username='testuser1', password='TestPassword123')

    def test_watch_pal(self):
        url = reverse('inqpal:add_pal')

        response = self.client.post(url, {'pal_id': self.account2.id, 'do': 'Watch'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, 'not an ajax respone when unwatching pal')
        self.assertIn('success', response.json(), 'failed to watch pal')

        self.assertTrue(self.account1.friends.filter(id=self.account2.id).exists(), 'added pal is not added to the models infomation')

    def test_unwatch_pal(self):
        self.account1.friends.add(self.account2)

        url = reverse('inqpal:add_pal')

        response = self.client.post(url, {'pal_id': self.account2.id, 'do': 'Unwatch'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200, 'not an ajax respone when unwatching pal')
        self.assertIn('success', response.json(), 'failed to unwatch pal')

        self.assertFalse(self.account1.friends.filter(id=self.account2.id).exists(), 'added pal in not removed from the models information')

    def test_find_your_pals_section(self):
        response = self.client.get(reverse('inqpal:add_pal'))
        content = response.content.decode()

        self.assertIn('<h2 id = \'search_box_title\'>Find Your Pals:</h2>', content, '"Find Your Pals" heading is missing.')
        self.assertIn('<input id="search_box_input"', content, 'Search input box is missing.')
        self.assertIn('<input type="reset" id = \'clear_button\' value = \'&#x2b59;\'>', content, 'Clear button is missing.')
        self.assertIn('<div id = \'add_pal_results\'>', content, 'Results container is missing.')

    def test_csrf_token_present(self):
        response = self.client.get(reverse('inqpal:add_pal'))
        content = response.content.decode()

        self.assertIn('<input type="hidden" name="csrfmiddlewaretoken"', content, 'CSRF token is missing from add pal form')

    def test_javascript_variables_and_script(self):
        response = self.client.get(reverse('inqpal:add_pal'))
        content = response.content.decode()

        self.assertIn('<script src="/static/js/add_pal.js">', content, 'JavaScript file is not being loaded.')

    def test_search_functionality_ui_elements(self):

        response = self.client.get(reverse('inqpal:add_pal'))
        content = response.content.decode()

        self.assertIn('<span id="search_box_icon">&#x2315;</span>', content, 'Search box icon is missing.')
        self.assertIn('<div id = \'search_area\'>', content, 'Search area container is missing.')

    def test_watch_button_presence(self):
        response = self.client.get(reverse('inqpal:add_pal'))
        content = response.content.decode()

        self.assertIn('class="watch_button"', content, 'Watch button is missing.')
    

class CreatePostTests(TestCase):



    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')
        self.client.login(username='testuser', password='TestPassword123')

    def tearDown(self):
        for post in Post.objects.all():
            post.delete()
        for category in Category.objects.all():
            category.delete()
        super().tearDown()
    

    def make_image(self):
        return SimpleUploadedFile("test_image.jpg", b"test_image", content_type="image/jpeg")

    def make_category(self):
        image = self.make_image()
        test_category = Category.objects.get_or_create(name='test_category',description='test_desc',picture=image)[0]
        test_category.save()
        return test_category
    
    def make_post(self):
        self.make_category()
        image = self.make_image()
        return self.client.post(reverse('inqpal:make_post'), {
            'image': image,
            'text': 'test_text',
            'category': "test_category"
        })
        
    
    def test_redirect_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('inqpal:make_post'))
        self.assertRedirects(response, f"{reverse('inqpal:login')}?next={reverse('inqpal:make_post')}", status_code=302, msg_prefix="Logged out user was not redirected to login page.")


    def test_no_image_chosen(self):
        response = self.client.post(reverse('inqpal:make_post'), {
            'category': "test_category",
            'text': 'test_text',
        })
        content = response.content.decode()
        self.assertIn('Error while processing post please try again', content, 'when image is not sent to the server an error message is not shown')


    def test_no_category_chosen(self):
        image = self.make_image()
        response = self.client.post(reverse('inqpal:make_post'), {
            'image': image,
            'text': 'test_text',
        })
        content = response.content.decode()
        self.assertIn('Error while processing post please try again', content, 'when cateogry is not sent to the server an error message is not shown')
    
    def test_no_text_input(self):
        image = self.make_image()
        response = self.client.post(reverse('inqpal:make_post'), {
            'image': image,
            'category': "test_category",
        })
        content = response.content.decode()
        self.assertIn('Error while processing post please try again', content, 'when text is not sent to the server an error message is not shown')

    def test_name_present(self):
        response = self.client.get(reverse('inqpal:make_post'))
        content = response.content.decode()
        self.assertIn('testuser', content, 'username does not show up on make_post')

    def test_post_is_created(self):
        post = self.make_post()
        self.assertTrue(Post.objects.exists() , 'post is not created with valid inputs')

    def test_post_is_added_to_account(self):
        post = self.make_post()
        self.assertEqual(self.account, Post.objects.first().creator, 'post is not added to the correct user')

    def test_post_is_added_to_category(self):
        post = self.make_post()
        self.assertEqual(Category.objects.first(), Post.objects.first().category, 'post is not added to the correct category')

    def test_post_has_correct_roars_and_comments(self):
        post = self.make_post()
        self.assertEqual(0, Post.objects.first().roars.all().count(), 'post has roars when noone has roared it')

    def test_post_has_correct_text(self):
        post = self.make_post()
        self.assertEqual('test_text', Post.objects.first().text, 'post has incorrect text')

    def test_post_has_image(self):
        post = self.make_post()
        self.assertIn('test_image.jpg', str(Post.objects.first().image), 'post has incorrect image')

    def test_baked_in_text_present(self):
        response = self.client.get(reverse('inqpal:make_post'))
        content = response.content.decode()
        self.assertIn('Create a Post', content, '"Create a Post" does not show up on make_post')
        self.assertIn('Enter your description', content, '"Enter your description" does not show up on make_post')
        self.assertIn('Select a Category', content, '"Select a Category" does not show up on make_post')
        self.assertIn('cancel', content, '"cancel" does not show up on make_post')
        self.assertIn('post', content, '"post" doespost not show up on make_post')
    
    def test_no_image_selected_shows_deafult(self):
        response = self.client.get(reverse('inqpal:make_post'))
        content = response.content.decode()
        self.assertIn('<img id = \'picture_preview\' src = "/static/images/noImageSelected.png"/>', content, 'default image not showing when no image has been slected')

class DisplayPostTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')
        self.client.login(username='testuser', password='TestPassword123')

    def make_other_account(self):
        other_user = User.objects.create_user(username='testuser2', email='test2@example.com', password='TestPassword321')
        other_account = Account.objects.create(user=other_user, fav_dino='T-Rex')
        return other_account

    def make_category(self):
        image = "chernobylFox.jpg"
        test_category = Category.objects.get_or_create(name='test_category',description='test_desc',picture=image)[0]
        test_category.save()
        return test_category
    
    def make_post(self):
        category = self.make_category()
        image = "chernobylFox.jpg"
        test_post = Post.objects.get_or_create(
            creator = self.account,
            image=image,
            text='test post 123',
            category=category)[0]
        test_post.save()
        return test_post
    
    def test_post_comment(self):
        post = self.make_post()
        response = self.client.post(reverse('inqpal:trending'), {
            'post': post.id,
            'submit':'post',
            'text':'test comment 123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(text='test comment 123').exists())

    def test_post_delete_comment(self):
        post = self.make_post()
        comment = Comment.objects.get_or_create(post=post,text='test comment 123',creator=self.account)[0]
        comment.save()
        response = self.client.post(reverse('inqpal:trending'), {
            'comment': comment.id,
            'submit':'delete',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Comment.objects.filter(text='test comment 123').exists())

    def test_post_roar(self):
        post = self.make_post()
        response = self.client.post(reverse('inqpal:trending'), {
            'post': post.id,
            'submit':'roar',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.roars.count(), 1)
    
    def test_post_roar(self):
        post = self.make_post()
        post.roars.add(self.account)
        response = self.client.post(reverse('inqpal:trending'), {
            'post': post.id,
            'submit':'unroar',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(post.roars.count(), 0)

    def test_roar_button_with_account(self):
        self.make_post()
        response = self.client.get(reverse('inqpal:trending'))
        self.assertTrue(b"roar_form" in response.content)

    def test_unroar_button_when_roared(self):
        post = self.make_post()
        post.roars.add(self.account)
        response = self.client.get(reverse('inqpal:trending'))
        self.assertTrue(b"unroar_form" in response.content)

    def test_no_roar_button_no_account(self):
        self.make_post()
        self.client.logout()
        response = self.client.get(reverse('inqpal:trending'))
        self.assertFalse(b"roar_form" in response.content)

    def test_delete_button_your_comment(self):
        post = self.make_post()
        comment = Comment.objects.get_or_create(post=post,text='test comment 123',creator=self.account)[0]
        comment.save()
        response = self.client.get(reverse('inqpal:trending'))
        self.assertTrue(b"delete_comment" in response.content)

    def test_delete_button_your_comment(self):
        post = self.make_post()
        otherAccount = self.make_other_account()
        comment = Comment.objects.get_or_create(post=post,text='test comment 123',creator=otherAccount)[0]
        comment.save()
        response = self.client.get(reverse('inqpal:trending'))
        self.assertFalse(b"delete_comment" in response.content)

    def test_display_error_no_posts(self):
        response = self.client.get(reverse('inqpal:trending'))
        self.assertTrue(b"Error: No posts to show!" in response.content)

    def test_display_post_and_comment(self):
        post = self.make_post()
        Comment.objects.get_or_create(post=post,creator=self.account,text="test comment 123")
        response = self.client.get(reverse('inqpal:trending'))
        self.assertTrue(b"test post 123" in response.content)
        self.assertTrue(b"test comment 123" in response.content)

class CategoriesTests(TestCase):
    def make_category(self):
        image = "chernobylFox.jpg"
        test_category = Category.objects.get_or_create(name='test_category',description='test_desc',picture=image)[0]
        test_category.save()
        return test_category
    
    def test_display_error_no_categories(self):
        response = self.client.get(reverse('inqpal:categories'))
        self.assertTrue(b"Error: No categories to show!" in response.content)

    def test_display_categories(self):
        self.make_category()
        response = self.client.get(reverse('inqpal:categories'))
        self.assertTrue(b"test_category" in response.content)

class ShowCategoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')
        self.client.login(username='testuser', password='TestPassword123')

    def make_category(self):
        image = "chernobylFox.jpg"
        test_category = Category.objects.get_or_create(name='test_category',description='test_desc',picture=image)[0]
        test_category.save()
        return test_category
    
    def make_other_category(self):
        image = "chernobylFox.jpg"
        test_category = Category.objects.get_or_create(name='test_category_2',description='test_desc',picture=image)[0]
        test_category.save()
        return test_category
    
    def make_post(self):
        category = self.make_category()
        image = "chernobylFox.jpg"
        test_post = Post.objects.get_or_create(
            creator = self.account,
            image=image,
            text='test post 123',
            category=category)[0]
        test_post.save()
        return test_post
    
    def test_display_error_no_posts_when_wrong_cat(self):
        self.make_other_category()
        self.make_post()
        response = self.client.get(reverse('inqpal:show_category', kwargs={'category_name':'test_category_2'}))
        self.assertTrue(b"Error: No posts to show!" in response.content)

    def test_display_post_when_in_cat(self):
        self.make_other_category()
        post = self.make_post()
        Comment.objects.get_or_create(post=post,creator=self.account,text="test comment 123")
        response = self.client.get(reverse('inqpal:show_category', kwargs={'category_name':'test_category'}))
        self.assertTrue(b"test post 123" in response.content)
        self.assertTrue(b"test comment 123" in response.content)

class TestPalsPosts(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')
        self.client.login(username='testuser', password='TestPassword123')

    def make_accounts(self):
        user1 = User.objects.create_user(username='testuser2', email='test2@example.com', password='TestPassword123')
        account1 = Account.objects.create(user=user1, fav_dino='Brontosaurus')
        user2 = User.objects.create_user(username='testuser3', email='test3@example.com', password='TestPassword123')
        account2 = Account.objects.create(user=user2, fav_dino='Argentinasaurus')
        return [account1,account2]

    def make_category(self):
        image = "chernobylFox.jpg"
        test_category = Category.objects.get_or_create(name='test_category',description='test_desc',picture=image)[0]
        test_category.save()
        return test_category
    
    def make_post(self,account):
        category = self.make_category()
        image = "chernobylFox.jpg"
        test_post = Post.objects.get_or_create(
            creator = account,
            image=image,
            text='test post 123',
            category=category)[0]
        test_post.save()
        return test_post
    
    def test_display_error_no_posts_when_not_pals(self):
        accounts = self.make_accounts()
        self.account.friends.add(accounts[0])
        self.make_post(accounts[1])
        response = self.client.get(reverse('inqpal:palsposts'))
        self.assertTrue(b"Error: No posts to show!" in response.content)

    def test_display_post_when_pals(self):
        accounts = self.make_accounts()
        self.account.friends.add(accounts[0])
        post = self.make_post(accounts[0])
        Comment.objects.get_or_create(post=post,creator=self.account,text="test comment 123")
        response = self.client.get(reverse('inqpal:show_category', kwargs={'category_name':'test_category'}))
        self.assertTrue(b"test post 123" in response.content)
        self.assertTrue(b"test comment 123" in response.content)
        
class MyAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')
        
        self.category = Category.objects.create(name="Test Category", description="A test category", picture="path/to/picture")
        for i in range(10):
            Post.objects.create(creator=self.account, text=f"Post {i}", category=self.category)
            
        self.watchers = []
        for i in range(1,6):
            watcher_user = User.objects.create_user(username=f"watcher{i}", password=f"watcher{i}password")
            watcher_account = Account.objects.create(user=watcher_user, fav_dino=f"FavDino{i}")
            self.watchers.append(watcher_account)
            
        for watcher in self.watchers:
            watcher.friends.add(self.account)
            
        self.friends = []
        for i in range(1,4):
            friend_user = User.objects.create_user(username=f"friend{i}", password=f"friend{i}password")
            friend_account = Account.objects.create(user=friend_user, fav_dino=f"FavDino{i}")
            self.friends.append(friend_account)
            
        for friend in self.friends:
            self.account.friends.add(friend)
            
        self.client.login(username='testuser', password='TestPassword123')
    
    def test_my_account_page_can_be_accessed(self):
        response = self.client.get(reverse("inqpal:my_account"))
        self.assertEqual(response.status_code, 200)
        
    def test_redirect_to_login_page_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("inqpal:my_account"))
        expectedURL = reverse("inqpal:login") + f"?next={reverse('inqpal:my_account')}"
        self.assertRedirects(response, expectedURL)
        
    def test_correctly_shows_user_data(self):
        response = self.client.get(reverse("inqpal:my_account"))
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.account.fav_dino)
        self.assertContains(response, f"{Post.objects.filter(creator=self.account).count()} posts")
        self.assertContains(response, f"{self.account.watchers.count()} watchers")
        self.assertContains(response, f"{self.account.friends.count()} pals")
    
    def test_paging_functionality(self):
        response = self.client.get(reverse("inqpal:my_account"),{"page": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("posts", response.context)
        
    def test_delete_post_functionality(self):
        post = Post.objects.first()
        response = self.client.post(reverse("inqpal:my_account"), {"selected_posts": [post.id]})
        selectedPostExists = Post.objects.filter(id=post.id).exists()
        self.assertFalse(selectedPostExists) 
        
class EditProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='TestPassword123')
        self.account = Account.objects.create(user=self.user, fav_dino='T-Rex')
    
    def test_redirect_to_login_page_if_not_logged_in(self):
        response = self.client.get(reverse("inqpal:edit_profile"))
        expectedURL = reverse("inqpal:login") + f"?next={reverse('inqpal:edit_profile')}"
        self.assertRedirects(response, expectedURL)
    
    def test_edit_with_invalid_input(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse("inqpal:edit_profile"), {"fav_dino": "",})
        self.account.refresh_from_db()
        self.assertNotEqual(self.account.fav_dino, "")

    def test_edit_with_incorrect_image_type(self):
        self.client.login(username="testuser", password="testpassword")
        invalidFile = SimpleUploadedFile("test_file.txt", b"random data", content_type="text/plain")
        response = self.client.post(reverse("inqpal:edit_profile"), {"fav_dino": "Iguanodon", "picture": invalidFile,})
        self.account.refresh_from_db()
        self.assertEqual(self.account.picture.name, "noImageSelected.png")