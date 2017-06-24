FROM rentme-py-base

RUN pip3 install flower && \
    mkdir -p /flower-db && \
    chmod a+rw /flower-db

COPY docker-utils/flowerconfig.py /flowerconfig.py

EXPOSE 5555

HEALTHCHECK --interval=5s --timeout=1s --retries=20 CMD curl --silent --fail http://localhost:5555/ || exit 1
CMD ["python3", "-m", "celery", "-E", "-A", "rentme.celery.celery_app", "flower", "--conf=/flowerconfig.py"]
