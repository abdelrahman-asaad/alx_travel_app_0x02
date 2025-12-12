# alx_travel_app/celery.py
import os
from celery import Celery

# اضبط environment variable على settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_travel_app.settings")

app = Celery("alx_travel_app")

# اقرأ إعدادات Celery من settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# يكتشف tasks من كل التطبيقات
app.autodiscover_tasks()
