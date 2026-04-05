from django.test import TestCase

# Create your tests here.

class BasicTest(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)