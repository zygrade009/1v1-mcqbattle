from django.utils import timezone
from datetime import timedelta

def default_expiration_time():
    return timezone.now() + timedelta(minutes=30)
