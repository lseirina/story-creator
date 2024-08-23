from django.test import TestCase
from stories import models

class ModelTests(TestCase):
    """ Tests for models."""

    def create_story(self):
        story = models.Story.objects.create(
            title='Unicorn',
            content='Blah, blah, blah'
        )

        self.assertEqual(str(story, story.title))
