FROM rentme-py-base

CMD ["python3", "-m", "celery", "-E", "-A", "rentme.data.importer.celery", "worker"]
