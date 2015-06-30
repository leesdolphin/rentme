import json
import django.http
from django.shortcuts import render, redirect
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

def search_rentals(request):
    x = api.load_rentals(**request.GET)
    return django.http.response.HttpResponse("<pre>" + json.dumps(x,
                                                                sort_keys=True,
                                                        indent=4))
