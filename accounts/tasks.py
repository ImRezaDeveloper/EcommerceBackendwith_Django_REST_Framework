from celery import shared_task
import time

@shared_task
def test_celery():
    time.sleep(5)
    print("celery-worker is working!@")
    return "done"