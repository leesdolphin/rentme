FROM rentme-py-base

HEALTHCHECK --interval=5s --timeout=1s --retries=20 CMD /venv/bin/celery inspect ping -A rentme.celery.celery_app -d celery@$HOSTNAME || exit 1
CMD ["python3", "-m", "celery", "-E", "-A", "rentme.celery.celery_app", "worker"]
