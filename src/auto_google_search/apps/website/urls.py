from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from auto_google_search.apps.website import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^search-history/(?P<search_record_id>\d+)/$', views.IndexView.as_view(), name='history'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
