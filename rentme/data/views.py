from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.list import BaseListView

from rentme.data import api, models
# from rentme.data.importer import catalogue


class LocalityView(ListView):
    model = models.catalogue.Locality
    template_name = 'rentme/locality_list.html'
    context_object_name = 'localities'


class LocalityDrilldownView(ListView):

    model = models.catalogue.Locality
    template_name = 'rentme/listings_all.html'
    context_object_name = 'listing_list'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        # if hasattr(self, 'locality_id'):
        #     qs = qs.filter(suburb__district__listing_id=int(self.locality_id))
        # if hasattr(self, 'district_id'):
        #     qs = qs.filter(suburb__district_id=int(self.district_id))
        if hasattr(self, 'suburb_id'):
            qs = qs.filter(suburb_id=int(self.district_id))
        return qs


class RentalListView(ListView):
    model = models.listings.Listing
    template_name = 'rentme/listings_all.html'
    context_object_name = 'listing_list'

    def get_queryset(self):
        suburbs = models.catalogue.Suburb.objects.filter(district_id__in=(47, 46, 45, 44))
        from pprint import pprint
        pprint(list(suburbs))

        qs = super().get_queryset()
        qs = qs.filter(rent_per_week__lt=500, rent_per_week__gt=200)
        qs = qs.filter(suburb__in=suburbs)
        pprint(list(qs))
        return qs


class RentalView(DetailView):
    template_name = 'rentme/listing_single.html'
    model = models.listings.Listing
