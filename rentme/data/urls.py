from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^localities$', views.LocalityView.as_view(), name='all-localities'),
    url(r'^localities/l/(?P<locality_id>[0-9]+)$', views.LocalityDrilldownView.as_view(), name='locality-drilldown'),
    url(r'^localities/d/(?P<district_id>[0-9]+)$', views.LocalityDrilldownView.as_view(), name='district-drilldown'),
    url(r'^localities/s/(?P<suburb_id>[0-9]+)$', views.LocalityDrilldownView.as_view(), name='suburb-drilldown'),
    url(r'^rentals/all$', views.RentalListView.as_view(), name='rentals.all'),
    url(r'^rentals/(?P<pk>[0-9]+)$', views.RentalView.as_view(), name='rentals.view'),
]
