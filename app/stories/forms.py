from django import forms
from stories import models


class StoryForm(forms.ModelForm):
    class Meta:
        model = models.Story
        fields = ['title', 'content']


class VoiceRecordingForm(forms.ModelForm):
    class Meta:
        model = models.VoiceRecording
        fields = ['file']


class EditTranscriptionForm(forms.ModelForm):
    class Meta:
        model = models.VoiceRecording
        fields = ['transcription']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.is_edited = True
        if commit:
            instance.save()

        return instance
