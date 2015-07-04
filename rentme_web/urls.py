from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'all-localities', views.list_all_locality, name='all-localities'),
    url(r'load-localities', views.load_all_locality, name='load-localities'),
    url(r'rentals/load-from-search', views.load_search_rentals,
        name='rentals/load-from-search'),
    url(r'rentals/load/(?P<id>[0-9]+)', views.load_rental, name='rentals/load'),
    url(r'rentals/all', views.all_rentals,
        name='rentals/all'),
    url(r'rentals/rental/(?P<id>[0-9]+)', views.one_rental,
        name='rentals/rental')
]
