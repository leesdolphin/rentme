
from aioutils.celery import asyncio_task
from celery.utils.log import get_task_logger

from rentme.celery.celery_app import app
from rentme.raw.models.members import Member
from rentme.raw.importer.data_migrations._utils import migrate_merge_model
from rentme.data.models import members


logger = get_task_logger(__name__)


@asyncio_task(app, ignore_result=True, rate_limit='5/s')
async def migrate_member(member_id, *, loop):
    old_member = Member.objects.get(member_id=member_id)
    old_profile = old_member.member_profile.first()
    new_member = migrate_merge_model(
        [old_member, old_profile],
        members.Member,
    )
    new_member.save()
    return new_member
