import asyncio
import math

from celery.utils.log import get_task_logger
from django.utils import timezone
from trademe.errors import ClassifiedExpiredError

from rentme.data.importer.celery import app
from rentme.data.importer.cleanup import clean_related_tables
from rentme.data.importer.utils import asyncio_task
from rentme.data.importer.utils import get_trademe_api, get_trademe_session
from rentme.data.models.listing import Listing, ListingPrice, PricePeriodEnum


logger = get_task_logger(__name__)


@asyncio_task(app)
async def postprocess_listing(listing_id, *, _loop):
    process_listing_price(listing_id)


def process_listing_price(listing_id):
    listing = Listing.objects.get(listing_id=listing_id)
    price_display = listing.price_display
    dollars, _, per_unit = price_display.partition(' per ')
    if not per_unit:
        logger.warning('Unable to parse price information for listing '
                       '%(listing_id)s. Given Price: %(price_display)r.'
                       'Failure reason: %(failure_reason)s',
                       {'listing_id': listing_id,
                        'price_display': price_display,
                        'failure_reason': 'price.partition failed'})
        return
    if dollars[0] != '$':
        logger.warning('Unable to parse price information for listing '
                       '%(listing_id)s. Given Price: %(price_display)r.'
                       'Failure reason: %(failure_reason)s',
                       {'listing_id': listing_id,
                        'price_display': price_display,
                        'failure_reason': 'dollar amount with no "$"'})
        return
    dollars = dollars[1:].replace(',', '')
    try:
        dollar_num = int(dollars)
    except:
        logger.warning('Unable to parse price information for listing '
                       '%(listing_id)s. Given Price: %(price_display)r.'
                       'Failure reason: %(failure_reason)s',
                       {'listing_id': listing_id,
                        'price_display': price_display,
                        'failure_reason': 'dollar amount not integer'})
        return

    if per_unit == 'week':
        per_unit_enum = PricePeriodEnum.WEEK
    elif per_unit == 'month':
        per_unit_enum = PricePeriodEnum.MONTH
    else:
        logger.warning('Unable to parse price information for listing '
                       '%(listing_id)s. Given Price: %(price_display)r.'
                       'Failure reason: %(failure_reason)s',
                       {'listing_id': listing_id,
                        'price_display': price_display,
                        'failure_reason': 'unkown price period'})
        return
    listing_price, _ = ListingPrice.objects.get_or_create(
        dollars=dollar_num, period=per_unit_enum)
    listing.price = listing_price
    listing.save()
