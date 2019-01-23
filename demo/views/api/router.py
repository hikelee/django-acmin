from rest_framework.routers import DefaultRouter


class Router(DefaultRouter):

    def get_default_basename(self, viewset):
        return viewset.Meta.model.__name__.lower()
