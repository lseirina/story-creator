from django import forms
from stories import models


class StoryForm(forms.ModelForm):
    class Meta:
        model = models.Story
        fields = ['title', 'content']


class VoiceRecording(forms.ModelForm):
    class Meta:
        model = models.VoiceRecording
        fields = ['file']