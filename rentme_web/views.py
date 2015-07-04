import json
import django.http
from django.shortcuts import render, redirect, get_object_or_404
from rentme_web import models, api

# Create your views here.

def load_all_locality(request):
    api.load_trademe_locality_information()
    return redirect('all-localities')

def list_all_locality(request):
    localities = models.TradeMeLocality.objects.order_by('name').all()
    count = models.TradeMeLocality.objects.count()
    context = {'localities': localities, 'c': count}
    return render(request, 'rentme/locality_all.html', context)

def load_search_rentals(request):
    kwargs = {key: val for key, val in request.GET.items()}
    x = api.search_rentals(**kwargs)
    return django.http.response.HttpResponse("Loaded " + len(x) + " properties")

def load_rental(request, id):
    x = api.load_rental(id)
    return django.http.response.HttpResponse("Loaded property")

def all_rentals(request):
    context = {}
    models.TradeMeListing.objects.filter(
        Q()
    )
    context['listing_list'] = []

    return render(request, 'rentme/listings_all.html', context)

def one_rental(request, id):
    listing = get_object_or_404(models.TradeMeListing, id=id)
    print(dir(listing))
    context = {'listing': listing}
    same_loc_listings = set(listing.location.trademelisting_set.all())
    context['similar_location_listings'] = same_loc_listings
    return render(request, 'rentme/listing_single.html', context)
