import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.urls import reverse

from book.models import Author, Book, Publisher
from category.models import Category
from user.models import Reviews, Favorite, Subscriber
from main.models import BookOffer


User = get_user_model()


class UserModelTest(TestCase):
    def test_validate_birth_date_too_young(self):
        """Пользователь младше 16 лет — ошибка"""
        with self.assertRaises(ValidationError):
            User(date_of_birth=date.today() - relativedelta(years=15)).full_clean()

    def test_validate_birth_date_too_old(self):
        """Дата рождения раньше 1950 года — ошибка"""
        with self.assertRaises(ValidationError):
            User(date_of_birth=date(1949, 12, 31)).full_clean()

    def test_photo_default_value(self):
        """Фото по умолчанию установлено правильно"""
        user = User.objects.create(username='testuser')
        self.assertEqual(user.photo.name, 'users/profile_pictures/default.png')


class SubscriberModelTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')

    def test_self_subscription_prevented(self):
        """Запрещено подписываться на самого себя"""
        with self.assertRaises(Exception):
            Subscriber.objects.create(subscriber=self.user1, subscribed_to=self.user1)

    def test_unique_pair(self):
        """Подписка между двумя пользователями может быть только одна"""
        Subscriber.objects.create(subscriber=self.user1, subscribed_to=self.user2)
        with self.assertRaises(Exception):
            Subscriber.objects.create(subscriber=self.user1, subscribed_to=self.user2)

    def test_str_representation(self):
        sub = Subscriber.objects.create(subscriber=self.user1, subscribed_to=self.user2)
        self.assertEqual(str(sub), f"{self.user1.username} -> {self.user2.username}")


class BaseViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.author = Author.objects.create(name='Test Author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.category = Category.objects.create(name='Fiction')

        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publisher=self.publisher,
            release_year=2020
        )
        self.book.category.add(self.category)

        self.book_offer = BookOffer.objects.create(
            user=self.user,
            book=self.book,
            edition_year=2020,
            description='Great book!',
            is_published=True,
            is_active='Active'
        )

        # Create a test image
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=tempfile.NamedTemporaryFile(suffix=".jpg").read(),
            content_type='image/jpeg'
        )


class ProfileViewTest(BaseViewTest):
    def test_profile_view_renders_correctly(self):
        response = self.client.get(reverse('profile:profile', kwargs={'username': self.user.username}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/my_profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_profile_edit_form(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile:edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile/profile-edit.html')


class ProfileEditViewTest(BaseViewTest):
    def test_profile_edit_updates_fields(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'New',
            'last_name': 'Name',
            'username': 'newusername',
        }
        response = self.client.post(reverse('profile:edit'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        updated_user = get_user_model().objects.get(pk=self.user.pk)
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'Name')
        self.assertEqual(updated_user.username, 'newusername')


class PasswordChangeViewTest(BaseViewTest):
    def test_password_change_works(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'old_password': 'testpass123',
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
        }
        response = self.client.post(reverse('profile:change-password'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        updated_user = get_user_model().objects.get(pk=self.user.pk)
        self.assertTrue(updated_user.check_password('newpassword123'))


class ToggleFavoriteViewTest(BaseViewTest):
    def test_toggle_favorite_add_and_remove(self):
        self.client.login(username='testuser', password='testpass123')
        offer = BookOffer.objects.create(
            user=self.user,
            book=self.book,
            edition_year=2020,
            description='Another book',
            is_published=True,
            is_active='Active'
        )
        # Add to favorite
        response = self.client.post(reverse('book:toggle-favorite'), {'offer_id': offer.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_favorite'])
        self.assertTrue(Favorite.objects.filter(user=self.user, offer=offer).exists())

        # Remove from favorite
        response = self.client.post(reverse('book:toggle-favorite'), {'offer_id': offer.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['is_favorite'])
        self.assertFalse(Favorite.objects.filter(user=self.user, offer=offer).exists())


class SubscribeViewTest(BaseViewTest):
    def test_subscribe_unsubscribe(self):
        self.client.login(username='testuser', password='testpass123')
        another_user = get_user_model().objects.create_user(
            username='another',
            password='anotherpass'
        )
        # Subscribe
        response = self.client.post(reverse('profile:subscribe'), {
            'subscriber_id': self.user.id,
            'subscriber_to_id': another_user.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['is_subscribed'])
        self.assertTrue(Subscriber.objects.filter(subscriber=self.user, subscribed_to=another_user).exists())

        # Unsubscribe
        response = self.client.post(reverse('profile:subscribe'), {
            'subscriber_id': self.user.id,
            'subscriber_to_id': another_user.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()['is_subscribed'])
        self.assertFalse(Subscriber.objects.filter(subscriber=self.user, subscribed_to=another_user).exists())
