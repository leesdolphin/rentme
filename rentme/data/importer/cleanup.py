from celery.utils.log import get_task_logger
from django.db import transaction
from django.db.models import Count

from rentme.data.importer.celery import app
from rentme.data.models import listing


logger = get_task_logger(__name__)


@app.task
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
        print(total_removed, removal_stats)
        if removal_stats.get('web.Listing', 0) > 0:
            raise Exception('*void screaming*')
