from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rentme.api import views

urlpatterns = format_suffix_patterns([
    url(r'^listings/$', views.ListingList.as_view()),
    # url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
])
