"""Tests for views."""
from django.test import TestCase, Client
from django.urls import reverse
from stories.views import story_list


STORIES_URL = reverse('story_list')

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()


def test_view_correct_templates(self):
    """Test the view uses correct templates."""
    res = self.client.get(STORIES_URL)
    self.assertEqual(res.status_code, 200)
    self.assertTemplateUsed(res, 'stories/story_list.html')
