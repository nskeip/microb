DEBUG=False
DATABASE_URI = 'sqlite:///micro.db'

try:
    from settings_local import *
except ImportError:
    pass
