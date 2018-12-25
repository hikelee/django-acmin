from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView

from demo import urls

urlpatterns = urls.get_patterns()
urlpatterns += [
    path('', RedirectView.as_view(url=settings.INDEX_URL))
]
