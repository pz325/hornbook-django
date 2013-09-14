import sys
import os.path
sys.path.insert(1, os.path.join(os.path.abspath('.'), 'libs'))

import django
print(django.get_version())
