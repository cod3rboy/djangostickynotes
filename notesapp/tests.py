from django.test import TestCase
from django.urls import reverse


class HomepageTest(TestCase):

    def test_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
