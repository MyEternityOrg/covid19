from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from .views import person_covid

urlpatterns = [
                  path('', person_covid, name='person_covid'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)