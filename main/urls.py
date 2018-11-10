import django.apps
from django.contrib import admin
from django.urls import path
from django.conf import settings
from demo import urls
from django.views.generic import RedirectView

for model in django.apps.apps.get_models():
    if not admin.site.is_registered(model):
        admin.site.register(model)

urlpatterns = urls.get_patterns()
urlpatterns += [
    path('django-admin/', admin.site.urls),
    path('', RedirectView.as_view(url=settings.INDEX_URL))
]
