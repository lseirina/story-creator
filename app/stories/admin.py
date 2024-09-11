from django.contrib import admin
from stories import models


admin.site.register(models.Story)
admin.site.register(models.VoiceRecording)