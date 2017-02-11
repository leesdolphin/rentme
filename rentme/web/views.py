import django.http
from django.shortcuts import redirect
from django.views.generic import ListView


from rentme.celery import catalogue
from rentme.web import api, models


class LocalityView(ListView):
    model = models.catalogue.Locality
    template_name = 'rentme/locality_list.html'
    context_object_name = 'localities'


def load_all_base_data(request):
    catalogue.reload_localities.apply_async()
    catalogue.reload_categories.apply_async()
    catalogue.reload_membership_localities.apply_async()
    return redirect('home')


def load_search_rentals(request):
    kwargs = {key: val for key, val in request.GET.items()}
    x = api.search_rentals(**kwargs)
    return django.http.response.HttpResponse('Loaded ' + str(len(x)) +
                                             ' properties')


def load_rental(request, id):
    # x = api.load_rental(id)
    return django.http.response.HttpResponse('Loaded property')
