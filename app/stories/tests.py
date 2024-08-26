from django.test import TestCase
"""SimpleUploadedFile — это класс, который используется в тестах.
   Он позволяет имитировать процесс загрузки файла, создавая объект файла,
   который можно использовать для тестирования."""
from django.core.files.uploadedfile import SimpleUploadedFile
from stories.models import Story, VoiceRecording


class ModelTests(TestCase):
    """ Tests for models."""
    def setUp(self):
        self.story = Story.objects.create(
            title='Sample Story',
            content='Sample content'
        )

    def create_story(self):
        """Test creating a story model."""
        story = Story.objects.create(
            title='Unicorn',
            content='Blah, blah, blah'
        )

        self.assertEqual(str(story, story.title))

    def create_voice_recording(self):
        """Префикс b перед строкой в Python обозначает, что строка является байтовой,
        а не обычной строкой Unicode."""
        audio_file = SimpleUploadedFile(file_name='sample.mp3',
                                        content=b'file_content',
                                        content_type='audio/mpeg')
        recording = VoiceRecording.objects.create(
            story=self.story,
            file=audio_file,
            transcription='Sample transcription'
        )

        self.assertEqual(VoiceRecording.objects.count(), 1)
        self.assertEqual(recording.story, self.story)
        self.assertEqual(recording.transcription, 'Sample transcription')
        self.assertTrue(recording.file.filename.endswith('sample.emp3'))
