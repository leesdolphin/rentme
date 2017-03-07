FROM rentme-py-base

RUN pip3 install flower

ADD docker-utils/flowerconfig.py /flowerconfig.py

EXPOSE 5555

CMD ["python3", "-m", "celery", "-E", "-A", "rentme.data.importer.celery", "flower", "--conf=/flowerconfig.py"]
