from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from rentme.data.importer.models import CachedResponse
from rentme.data.models import listing


logger = get_task_logger(__name__)


@app.task(ignore_result=True, rate_limit='5/s')
def clean_related_tables():
    with transaction.atomic():
        to_remove = [
            listing.BroadbandTechnology.objects
                   .annotate(Count('listings'))
                   .filter(listings__count=0),
            listing.Agency.objects
                   .annotate(Count('listings'))
                   .filter(listings__count=0),
            listing.Photo.objects
                   .annotate(Count('listings'), Count('listing_photo_set'))
                   .filter(listings__count=0, listing_photo_set__count=0),
            listing.GeographicLocation.objects
                   .annotate(Count('listings'))
                   .filter(listings__count=0),
            listing.Attributes.objects
                   .annotate(Count('listings'))
                   .filter(listings__count=0),
        ]
        total_removed = 0
        removal_stats = {}
        for query in to_remove:
            count, stats = query.delete()
            total_removed += count
            for model, rm_count in stats.items():
                removal_stats[model] = removal_stats.get(model, 0) + rm_count
        if removal_stats.get('data.Listing', 0) > 0:
            raise Exception('*void screaming*')


@app.task(ignore_result=True, rate_limit='5/s')
def clean_cache_tables():
    CachedResponse.objects.filter(expiry__gte=timezone.now()).delete()
