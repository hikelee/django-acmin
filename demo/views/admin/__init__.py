from acmin.utils import import_submodules
from acmin.views import *


 


class BaseCreateView( AdminCreateView):
    pass


class BaseUpdateView( AdminUpdateView):
    pass


class BaseListView( AdminListView):
    pass


class BaseExportView( AdminExportView):
    pass


class BaseDeleteView( AdminDeleteView):
    pass


import_submodules(locals(), __name__, __path__)
