"""
Tests forms.
"""
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from stories.forms import StoryForm, VoiceRecordingForm, EditTranscriptionForm
from stories.models import Story, VoiceRecording
import tempfile


class StoryTest(TestCase):
    def test_story_form_valid(self):
        """Test create story if form is valid."""
        form_data = {'title': 'Sample title', 'content': 'It is content'}
        form = StoryForm(data=form_data)

        self.assertTrue(form.is_valid())

        story = form.save() # is used to save the data from a form into the corresponding model instance
        self.assertEqual(story.title, form_data['title'])


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class VoiceRecordingTests(TestCase):
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


class EditTranscriptionTests(TestCase):
    def setUp(self):
        audio_file = SimpleUploadedFile(
             'sample.mp3',
             b'file_content',
             content_type='audio/mpeg'
        )
        self.story = Story.objects.create(
            title='Sample title',
            content='It is content'
        )
        self.recording = VoiceRecording.objects.create(
            story=self.story,
            file=audio_file,
            transcription='It is transcription'
        )

    def test_is_edited_set_to_true(self):
        """Test is edited set to true after editing."""
        form = EditTranscriptionForm(
                data={'transcription': "Edited transcription"},
                instance=self.recording
            )

        self.assertTrue(form.is_valid())

        update_recording = form.save()

        self.assertTrue(update_recording.is_valid())
        self.assertEqual(update_recording.transcription, 'Edited Transcription')
