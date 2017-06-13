FROM rentme-py-base

HEALTHCHECK --interval=5s --timeout=1s --retries=20 CMD /venv/bin/celery inspect ping -A rentme.data.importer.celery -d celery@$HOSTNAME || exit 1
CMD ["python3", "-m", "celery", "-E", "-A", "rentme.data.importer.celery", "worker"]

COPY ["trademe", "rentme", "aioutils", "requirements.txt", "setup.py", "setup.cfg", "manage.py", "/code/"]
RUN /venv/bin/pip install -e /code
