"""
Tests forms.
"""
from django.test import TestCase
from stories.forms import StoryForm, VoiceRecordingForm


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