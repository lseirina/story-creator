"""Tests for views."""
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from stories.views import story_list
from stories.models import Story, VoiceRecording
import tempfile


STORIES_URL = reverse('story_list')


def detail_url(story_id):
    return reverse('story_detail', args=[story_id])


def recording_url(recording_id):
    return reverse('edit_transcription', args=[recording_id])


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
        self.assertTemplateUsed(res, 'story_list.html')

    # def test_context_data(self):
    #     """Test the view passes correct context data."""
    #     Story.objects.create(title='Story 1', content='It as a content')
    #     Story.objects.create(title='Story 2', content='It is a content')

    #     res = self.client.get(STORIES_URL)

    #     self.assertequal(res.status_code, 200)
    #     self.assertIn('stories', res.context)
    #     self.assertEqual(len(res.context['stories'], 2))

    def test_empty_list(self):
        """Test view handles empty story."""
        res = self.client.get(STORIES_URL)

        self.assertEqual(res.status_code, 200)
        self.assertIn('stories', res.context)
        self.assertEqual(len(res.context['stories']), 0)

    def test_detail_view_correct_templates(self):
        story = create_story()
        url = detail_url(story.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, 'story_detail.html')

    def test_story_detail_correct_content(self):
        """Test story_detail view contains correct cintent."""
        story = create_story()
        url = detail_url(story.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, story.title)
        self.assertContains(res, story.content)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class AddRecordingViewTests(TestCase):
    """"Tests for add recording view."""

    def setUp(self):
        self.story = create_story()
        self.client = Client()
        self.url = detail_url(self.story.id)

    # def test_add_recording_success(self):
    #     """Test add recording to story is successful."""
    #     audio_file = SimpleUploadedFile('sample.mp3',
    #                                     b'file_content',
    #                                     content_type='audio/mpeg')
    #     res = self.client.post(self.url, {'file': audio_file})

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(VoiceRecording.objects.filter(story=self.story).exists())
    #     recording = VoiceRecording.objects.get(story=self.story)
    #     self.assertEqual(recording.story, self.story)

    def test_add_recording_get_request(self):
        """Test add recording get request successful."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed('add_recording.html')


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class EditTranscription(TestCase):
    def setUp(self):
        self.client = Client()
        self.story = Story.objects.create(
            title='Test Title',
            content='Test Content.',
        )
        audio_file = SimpleUploadedFile(
            'sample.mp3',
            b'file_content',
            'audio/mpeg',
        )
        self.recording = VoiceRecording.objects.create(
            story=self.story,
            file=audio_file,
            transcription='Test transcription.'
        )

    def test_edit_transcription_success(self):
        """Test to edit recording is successful."""
        url = recording_url(self.recording.id)
        payload = {'transcription': 'Edited transcription'}
        res = self.client.post(url, payload)

        self.recording.refresh_from_db()
        self.assertEqual(res.status_code, 302)
        self.assertEqual(self.recording.transcription, payload['transcription'])

    def test_edit_transcription_form_display(self):
        """Test form display edit transcription."""
        url = recording_url(self.recording.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.recording.transcription)
        self.assertTemplateUsed(res, 'edit_transcription.html')

    # def test_edit_transcription_invalid_form(self):
    #     """Test invalid form edit transcription."""
    #     url = recording_url(self.recording.id)
    #     payload = {'transcription': ''}
    #     res = self.client.post(url, payload)

    #     self.recording.refresh_from_db()
    #     # self.assertContains(res, self.recording.transcription)
    #     self.assertFalse(self.recording.is_edited)

    def test_edit_transcription_recording_not_found(self):
        """Test edit transcription recordign not found return error."""
        url = recording_url(999)
        res = self.client.get(url)

        self.assertEqual(res.status_code, 404)

    def test_edit_transcription_redirect_on_success(self):
        """Test after edit transcription redirect is successful."""
        url1 = recording_url(self.recording.id)
        payload = {'transcription': 'New transcription.'}
        res = self.client.post(url1, payload)

        self.assertEqual(res.status_code, 302)
        url2 = detail_url(self.recording.id)
        self.assertRedirects(res, url2)
