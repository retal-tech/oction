"""
Testing views, models, urls.
"""
from django.test import TestCase


# Create your tests here.
class TestLandingView(TestCase):
    def test_landing_view_slash(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')

    def test_landing_view_404(self):
        response = self.client.get('/not-exist-bullshit-never-used')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')

