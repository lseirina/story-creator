from django.db import models


class Story(models.Model):
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VoiceRecording(models.Model):
    """related_name задает имя обратной связи, через которое обращаются
    к записям (VoiceRecording),
    связанным с определенной историей (Story).
    Без использования related_name доступ к связанным объектам происходит
    через автоматическое имя <model_name>_set,
    в вашем случае это было бы voicerecording_set."""
    story = models.ForeignKey(Story, related_name='recordings',
                              on_delete=models.CASCADE)
    file = models.FileField(upload_to='recordings/') # Параметр upload_to определяет путь, куда будут загружаться файлы на сервере.
    transcription = models.TextField(blank=True, null=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return f'Recording for story {self.story.title}'
