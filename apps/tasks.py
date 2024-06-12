from random import randint
from time import time

from celery import shared_task
from django.core.mail import send_mail

from root.settings import EMAIL_HOST_USER


@shared_task
def send_to_email(email):
    # email.content_subtype = 'html'
    password = randint(1000000, 9999999)
    start = time()
    send_mail('Confirm password', password, EMAIL_HOST_USER, [email])
    end = time()
    return {'email': email, 'time': int(end - start)}
