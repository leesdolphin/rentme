from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.list import BaseListView

from rentme.data import api
# from rentme.data.importer import catalogue


class LocalityView(ListView):
    # model = models.catalogue.Locality
    template_name = 'rentme/locality_list.html'
    context_object_name = 'localities'


class LocalityDrilldownView(ListView):

    # model = models.listing.Listing
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


class LocalityGraphView(BaseListView):
    # model = models.catalogue.Suburb
    # queryset = model.objects\
    #     .prefetch_related('adjacent_suburbs', 'listings')\
    #     .annotate(locality_name=F('district__locality__name'))
    context_object_name = 'suburbs'

    def render_to_response(self, context):
        suburbs = {}
        adjacency = set()
        for suburb in context['suburbs']:
            listings_count = suburb.listings.count()
            if listings_count == 0:
                continue
            suburbs[suburb.suburb_id] = {
                'id': suburb.suburb_id,
                'name': suburb.name,
                'locality': suburb.locality_name,
                'listings': listings_count,
            }
            for adj in suburb.adjacent_suburbs.all():
                if (adj.suburb_id, suburb.suburb_id) not in adjacency:
                    adjacency.add((suburb.suburb_id, adj.suburb_id))
        adj_lists = [
            dict(source=src_id, target=dst_id)
            for src_id, dst_id in adjacency
            if src_id in suburbs and dst_id in suburbs
        ]
        return JsonResponse(dict(
            nodes=list(suburbs.values()),
            links=adj_lists,
        ))


class RentalListView(ListView):
    # model = models.listing.Listing
    template_name = 'rentme/listing_all.html'
    context_object_name = 'listing_list'


class RentalView(DetailView):

    template_name = 'rentme/listing_single.html'
    # model = models.listing.Listing


def load_all_base_data(request):
    catalogue.reload_localities.apply_async()
    catalogue.reload_categories.apply_async()
    catalogue.reload_membership_localities.apply_async()
    return redirect('home')


def load_search_rentals(request):
    kwargs = {key: val for key, val in request.GET.items()}
    x = api.search_rentals(**kwargs)
    return HttpResponse('Loaded ' + str(len(x)) + ' properties')


def load_rental(request, id):
    x = api.load_rental(id)
    return HttpResponse('Loaded property')
