FROM rentme-py-base

CMD ["celery", "-E", "-A", "rentme.celery", "worker"]
