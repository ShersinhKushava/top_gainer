import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')

app = Celery('todo_project')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Define the beat schedule
app.conf.beat_schedule = {
    'fetch-top-gainers-every-3-minutes': {
        'task': 'todos.tasks.fetch_top_gainers_task',
        'schedule': crontab(minute='*/3', hour='9-10', day_of_week='1-5'),  # Every 3 minutes, 9-10 AM, Mon-Fri
    },
}
