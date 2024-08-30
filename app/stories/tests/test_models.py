from django.test import TestCase, override_settings
"""SimpleUploadedFile — это класс, который используется в тестах.
   Он позволяет имитировать процесс загрузки файла, создавая объект файла,
   который можно использовать для тестирования."""
from django.core.files.uploadedfile import SimpleUploadedFile
from stories.models import Story, VoiceRecording
import tempfile

"""Декоратор @override_settings  позволяет переопределять
любые настройки в settings.py
Функция tempfile.gettempdir() из стандартной библиотеки Python возвращает
путь к временной директории.
Эта директория будет автоматически очищена операционной системой"""
@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ModelTests(TestCase):
    """ Tests for models."""
    def setUp(self):
        self.story = Story.objects.create(
            title='Sample Story',
            content='Sample content'
        )

    def test_create_story(self):
        """Test creating a story model."""
        story = Story.objects.create(
            title='Unicorn',
            content='Blah, blah, blah'
        )

        self.assertEqual(str(story), story.title)

    def test_create_voice_recording(self):
        """Префикс b перед строкой в Python обозначает, что строка является
        байтовой, а не обычной строкой Unicode."""
        audio_file = SimpleUploadedFile('sample.mp3',
                                        b'file_content',
                                        content_type='audio/mpeg')
        recording = VoiceRecording.objects.create(
            story=self.story,
            file=audio_file,
            transcription='Sample transcription'
        )
        print(recording.file.name)
        self.assertEqual(VoiceRecording.objects.count(), 1)
        self.assertEqual(recording.story, self.story)
        self.assertEqual(recording.transcription, 'Sample transcription')

    def test_voice_recording_str(self):
        recording = VoiceRecording.objects.create(
            story=self.story,
            file=SimpleUploadedFile('sample.mp3',
                                    b'file_content',
                                    content_type='audio/mpeg'),
            transcription='Sample transcription'
        )

        self.assertEqual(str(recording),
                         f'Recording for story {self.story.title}')

    def test_delete_story_deletes_recording(self):
        VoiceRecording.objects.create(
            story=self.story,
            file=SimpleUploadedFile('sample.mp3',
                                    b'file_content',
                                    content_type='audio/mpeg')
        )
        self.story.delete()

        self.assertEqual(VoiceRecording.objects.count(), 0)

    def test_is_edited_false(self):
        """Test is_edited is false by default."""
        audio_file = SimpleUploadedFile('sample.mp3',
                                        b'file_content',
                                        content_type='audio/mpeg')
        recording = VoiceRecording(
            story=self.story,
            file=audio_file,
            transcription='Sampletranscription'
        )
        self.assertFalse(recording.is_edited)

    def test_is_edited_after_editing(self):
        """Test is_edited after editing is True."""
        audio_file = SimpleUploadedFile('sample.mp3',
                                        b'file_content',
                                        content_type='audio/mpeg')
        recording = VoiceRecording(
            story=self.story,
            file=audio_file,
            transcription='Sampletranscription'
        )
        recording.transcription = 'Editing transcription'
        recording.save()
        self.assertTrue(recording.is_edited)
