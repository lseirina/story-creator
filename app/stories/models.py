from django.db import models


class StoryModel(models.Model):
    title = models.CharField(max_length=255, blank=True)
    text = models.TextField()
    created_at = models.DataTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
