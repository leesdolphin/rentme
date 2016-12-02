import django.http
from django.db.models import Q
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
    return django.http.response.HttpResponse("Loaded " + str(len(x)) + " "
                                                                   "properties")

def load_rental(request, id):
    x = api.load_rental(id)
    return django.http.response.HttpResponse("Loaded property")

def delete_expired(request):
    api.delete_expired()
    return django.http.response.HttpResponse("Deleted all expired property")

def filtered_rentals(*other_filters):
    filters = (
                Q(rent_per_week__lt=475),
                Q(rent_per_week__gt=300),
                Q(bedrooms__gte=2),
              ) + other_filters
    return models.TradeMeListing.objects.filter(*filters)

def all_rentals(request):
    context = {}
    filters = []
    if not request.GET.get('all', None):
        filters = [Q(review__isnull=True) | Q(review__rating__gte=1)]
    context['listing_list'] = filtered_rentals(*filters).order_by('-review__rating', 'id')

    return render(request, 'rentme/listings_all.html', context)

def all_unrated_rentals(request):
    ls_all = filtered_rentals(Q(review__isnull=True)).order_by('id')
    context = {'listing_list': ls_all}

    return render(request, 'rentme/listings_all.html', context)


def one_rental(request, id):
    listing = get_object_or_404(models.TradeMeListing, id=id)
    print(listing.trademe_url)
    context = {'listing': listing}
    same_loc_listings = set(listing.location.trademelisting_set.all())
    if listing.location.accuracy in (1, 3):
        ##  Street or Address accuracy level
        context['similar_location_listings'] = same_loc_listings
        context['similar_location_photos'] = models.photos_cleanup([
            photo for ls in same_loc_listings for photo in ls.all_photos
        ])
    return render(request, 'rentme/listing_single.html', context)

def delete_rental(request, id):
    listing = get_object_or_404(models.TradeMeListing, id=id)
    listing.delete()
    return redirect('rentals.all')


def redirect_next_unrated_rental(request, id):
    try:
        next_rental = filtered_rentals(Q(review__isnull=True)).order_by('id')[0]
        return redirect('rentals.view', id=next_rental.id)
    except IndexError:
        return redirect('rentals.all')

def review_rental(request, id, rating):
    rating = rating.lower()
    listing = get_object_or_404(models.TradeMeListing, id=id)
    if rating in models.PropertyReview.MAPPING:
        rating = models.PropertyReview.MAPPING[rating]
        review, created = models.PropertyReview.objects.get_or_create(
            defaults={'rating': rating},
            property=listing
        )
        review.rating = rating
        review.save()
        listing.review = review
        listing.save()
        return redirect_next_unrated_rental(request, id)
    return redirect('rentals.view', id=id)


