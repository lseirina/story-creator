"""Tests for views."""
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from stories.views import story_list
from stories.models import Story, VoiceRecording


STORIES_URL = reverse('story_list')


def detail_url(story_id):
    return reverse('story_detail', args=[story_id])


def create_story(**params):
    """Create and return a new story."""
    defaults = {
        'title': 'Sample title',
        'content': 'It is a content'
    }

    defaults.update(params)

    story = Story.objects.create(**defaults)

    return story


class StoryViewTests(TestCase):
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
    story = create_story()
    url = detail_url(story.id)
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)
    self.assertTemplateUsed(res, 'stories/create_story.html')


def test_story_detail_correct_content(self):
    """Test story_detail view contains correct cintent."""
    story = create_story()
    url = detail_url(story.id)
    res = self.client.get(url)

    self.assertEqual(res.status_code, 200)
    self.assertContains(res, story.title)
    self.assertContains(res, story.content)


class AddRecordingViewTests(TestCase):
    """"Tests for add recording view."""

    def SetUp(self):
        self.story = create_story()
        self.client = Client()
        self.url = detail_url(self.story.id)

    def test_add_recording_success(self):
        """Test add recording to story is successful."""
        audio_file = SimpleUploadedFile('sample.mp3',
                                        b'file_content',
                                        content_type='audio/mpeg')
        res = self.client.post(self.story, {'file': audio_file})

        self.assertEqual(res.status_code, 302)
        self.assertTrue(VoiceRecording.objects.filter(story=self.story).exists())
        recording = VoiceRecording.objects.get(story=self.story)
        self.assertEqual(recording.story, self.story)

    def test_add_recording_get_request(self):
        """Test add recording get request successful."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('stories/add_recording.html')