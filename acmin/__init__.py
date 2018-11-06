VERSION = (0, 0, 8)
__version__ = '.'.join(map(str, VERSION))

default_app_config = 'acmin.apps.AcminConfig'


from . import utils
from . import views