from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class LoginPageTest(TestCase):

    def test_url_path(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


class SignupPageTest(TestCase):

    def test_url_path(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accountsapp/signup.html')


class PasswordResetPageTest(TestCase):

    def test_url_path(self):
        response = self.client.get('/accounts/password_reset/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_form.html')


class PasswordResetDonePageTest(TestCase):

    def test_url_path(self):
        response = self.client.get('/accounts/password_reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_done.html')


class PasswordResetCompletePageTest(TestCase):

    def test_url_path(self):
        response = self.client.get('/accounts/reset/done/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_reset_complete.html')


class PasswordChangePageTest(TestCase):

    def setUp(self):
        temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username=temp_user.username, password='passtemp123')
        self.assertTrue(login)

    def test_url_path(self):
        response = self.client.get('/accounts/password_change/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/password_change_form.html')


class ProfilePageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            username='tempuser123',
            first_name='temp',
            last_name='last_name',
            gender=get_user_model().Gender.MALE,
            email='tempuser123@email.com',
            password='passtemp123',
        )
        login = self.client.login(username=self.temp_user.username, password='passtemp123')
        self.assertTrue(login)

    def test_url_path(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accountsapp/profile.html')

    def test_template_has_context_siteuser(self):
        user_model = get_user_model()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context[user_model.__name__.lower()], None)
        self.assertIsInstance(response.context[user_model.__name__.lower()], user_model)
        self.assertEqual(response.context[user_model.__name__.lower()], self.temp_user)

    def test_page_data(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.temp_user.get_full_name())
        self.assertContains(response, self.temp_user.get_gender())
        self.assertContains(response, self.temp_user.username)
        self.assertContains(response, self.temp_user.email)

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)


class ProfileChangePageTest(TestCase):

    def setUp(self):
        self.temp_user = get_user_model().objects.create_user(
            first_name='temp',
            last_name='user',
            gender=get_user_model().Gender.MALE,
            email='tempuser123@email.com',
            username='tempuser123',
            password='passtemp123'
        )
        login = self.client.login(username=self.temp_user.username, password='passtemp123')
        self.assertTrue(login)

    def test_url_path(self):
        response = self.client.get('/profile/change/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('profile_change'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('profile_change'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accountsapp/profile_change.html')

    def test_profile_update(self):
        first_name = 'zoe'
        last_name = 'james'
        gender = str(get_user_model().Gender.FEMALE)
        email = 'zo3james@email.com'
        response = self.client.post(reverse('profile_change'), data={
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'email': email,
        })
        self.assertRedirects(response, reverse('profile'))
        self.temp_user = get_user_model().objects.get(pk=self.temp_user.id)
        self.assertEqual(self.temp_user.first_name, first_name)
        self.assertEqual(self.temp_user.last_name, last_name)
        self.assertEqual(self.temp_user.gender, gender)
        self.assertEqual(self.temp_user.email, email)

    def test_anonymous_user_redirect(self):
        self.client.logout()
        response = self.client.get(reverse('profile_change'))
        self.assertTrue(response.status_code, 302)
