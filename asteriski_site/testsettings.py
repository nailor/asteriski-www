import os.path
from asteriski_site.settings import *

current = os.path.dirname(__file__)

TEMPLATE_DIRS = (
    os.path.join(current, '..', 'templates'),
                 )

MEDIA_ROOT = os.path.join(current, '..', 'media')
