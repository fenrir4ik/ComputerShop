from celery import shared_task

def my_task():
    print('Task performed')