


# yourproject/celery.py
# celery is for setting periodic messeges

# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewelryshop.settings')

# app = Celery('jewelryshop')

# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Auto-discover tasks from all installed apps
# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')
