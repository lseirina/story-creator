from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VoiceRecording(models.Model):
    story = models.ForeignKey(Story, related_name='recordings',
                              on_delete=models.CASCADE)
    file = models.FileField(upload_to='recordings/')
    transcription = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Recording for story {self.story.title}'