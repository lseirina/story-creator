"""
Tests forms.
"""
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from stories.forms import StoryForm, VoiceRecordingForm
from stories.models import Story
import tempfile


class FormTest(TestCase):
    def test_story_form_valid(self):
        """Test create story if form is valid."""
        form_data = {'title': 'Sample title', 'content': 'It is content'}
        form = StoryForm(data=form_data)

        self.assertTrue(form.is_valid())

        story = form.save() # is used to save the data from a form into the corresponding model instance
        self.assertEqual(story.title, form_data['title'])

    def test_story_form_unvalid(self):
        """Test not to create story if form is not valid."""
        form_data = {'title': '', 'content': 'It is a content'}
        form = VoiceRecordingForm(data=form_data)

        self.assertFalse(form.is_valid())

    def test_recording_form_valid(self):
        """Test record audio file if form is valid."""
        audio_file = SimpleUploadedFile('sample.mp3',
                                        b'file_content',
                                        content_type='audio/mpeg')
        form = VoiceRecordingForm(files={'file': audio_file})
        story = Story.objects.create(title='Sample title',
                                     content='it is content')

        self.assertTrue(form.is_valid())

        recording = form.save(commit=False) # останавливает автоматическое сохранение формы в базу данных,
        # чтобы сделать дополнительные изменения перед сохранением
        recording.story = story
        recording.save()
        self.assertEqual(recording.file.size, len(b'file_content'))

    def test_recording_form_missing_file(self):
        """Test create form with missing file returns error."""
        form = VoiceRecordingForm({})
        self.assertFalse(form.is_valid())