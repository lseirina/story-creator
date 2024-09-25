from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'story_creator.settings')

app = Celery('story_creator')

app.cofig_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')