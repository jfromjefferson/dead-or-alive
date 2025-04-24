from celery import Celery
import os

celery_app = Celery(
    'worker',
    broker=os.environ.get('REDIS_BROKER'),
    backend=os.environ.get('REDIS_BACKEND'),
    include=['core.tasks']
)

celery_app.conf.beat_schedule = {
    'check-urls-every-60-seconds': {
        'task': 'core.tasks.check_all_urls',
        'schedule': 60.0,
    },
}
celery_app.conf.timezone = 'UTC'
