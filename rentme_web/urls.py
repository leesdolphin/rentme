from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'all-localities', views.list_all_locality, name='all-localities'),
    url(r'load-localities', views.load_all_locality, name='load-localities'),
]
