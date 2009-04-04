from datetime import datetime
from django.conf import settings

def now():
    if hasattr(settings, 'TEST_TIME'):
        return settings.TEST_TIME
    return datetime.now()
