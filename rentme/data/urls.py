from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^localities$', views.LocalityView.as_view(), name='all-localities'),
    url(r'^localities/l/(?P<locality_id>[0-9]+)$', views.LocalityDrilldownView.as_view(), name='locality-drilldown'),
    url(r'^localities/d/(?P<district_id>[0-9]+)$', views.LocalityDrilldownView.as_view(), name='district-drilldown'),
    url(r'^localities/s/(?P<suburb_id>[0-9]+)$', views.LocalityDrilldownView.as_view(), name='suburb-drilldown'),
    url(r'^localities.json$', views.LocalityGraphView.as_view(), name='json-localities'),
    # url(r'^load-localities$', views.load_all_locality, name='load-localities'),
    # url(r'^rentals/load/(?P<id>[0-9]+)$', views.load_rental, name='rentals.load'),
    # url(r'^rentals/all$', views.all_rentals, name='rentals.all'),
    # url(r'^rentals/all/unrated$', views.all_unrated_rentals, name='rentals.all.unrated'),
    url(r'^rentals/(?P<pk>[0-9]+)$', views.RentalView.as_view(), name='rentals.view'),
    # url(r'^rentals/(?P<id>[0-9]+)/delete$', views.delete_rental, name='rentals.delete'),
    # url(r'^rentals/(?P<id>[0-9]+)/review/(?P<rating>[a-zA-Z0-9]+)$', views.review_rental, name='rentals.review'),
]
