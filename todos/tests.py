from django.test import TestCase, Client

class TodoViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_returns_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)