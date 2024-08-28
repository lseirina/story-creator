"""Tests for views."""
from django.test import TestCase, Client
from django.urls import reverse
from stories.views import story_list


STORIES_URL = reverse('story_list')

def detail_url(story_id):
    return reverse('story_detail', args=[story_id])

class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()


def test_view_correct_templates(self):
    """Test the view uses correct templates."""
    res = self.client.get(STORIES_URL)
    self.assertEqual(res.status_code, 200)
    self.assertTemplateUsed(res, 'stories/story_list.html')


def test_context_data(self):
    """Test the view passes correct context data."""
    Story.objects.create(title='Story 1', content='It as a content')
    Story.objects.create(title='Story 2', content='It is a content')

    res = self.client.get(STORIES_URL)

    self.assertequal(res.status_code, 200)
    self.assertIn('stories', res.context)
    self.assertEqual(len(res.context['syories'], 2))


def test_empty_list(self):
    """Test view handles empty story."""
    res = self.client.get(STORIES_URL)

    self.assertEqual(res.status_code, 200)
    self.assertIn('stories', res.context)
    self.assertEqual(res.context['stories'], [])


def test_view_coorect_templates(self):
