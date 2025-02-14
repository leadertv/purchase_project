import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'purchase_project.settings')

app = Celery('purchase_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
