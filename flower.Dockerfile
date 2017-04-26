FROM rentme-py-base

RUN pip3 install flower && \
    mkdir -p /flower-db && \
    chmod a+rw /flower-db

ADD docker-utils/flowerconfig.py /flowerconfig.py

EXPOSE 5555

CMD ["python3", "-m", "celery", "-E", "-A", "rentme.data.importer.celery", "flower", "--conf=/flowerconfig.py"]
