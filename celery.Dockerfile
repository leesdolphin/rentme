FROM rentme-py-base

HEALTHCHECK --interval=1m --timeout=1s --retries=20 CMD /venv/bin/celery inspect ping -A rentme.celery.celery_app -d celery@$HOSTNAME || exit 1
CMD ["python3", "-m", "celery", "-A", "rentme.celery.celery_app", "worker", "--concurrency", "4", "--task-events", "--loglevel", "INFO"]

# "--task-events" \
# "--autoscale", "8,1", \
# "--loglevel", "INFO" \
