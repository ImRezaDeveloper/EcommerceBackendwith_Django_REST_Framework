import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CommerceCore_Scalable_EcommerceBackendwith_Django_REST_Framework.settings')

app = Celery("CommerceCore_Scalable_EcommerceBackendwith_Django_REST_Framework")
app.config_from_object('CommerceCore_Scalable_EcommerceBackendwith_Django_REST_Framework.settings', namespace='CELERY')
app.autodiscover_tasks()