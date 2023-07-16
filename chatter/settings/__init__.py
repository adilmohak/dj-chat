from .base import *
try:
	from .local import *
	live = False
except ImportError:
	live = True

if live:
    from .production import *