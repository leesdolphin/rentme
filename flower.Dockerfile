FROM rentme-py-base

RUN pip3 install flower

ADD docker-utils/flowerconfig.py /flowerconfig.py

EXPOSE 5555

CMD ["celery", "-E", "-A", "rentme.celery", "flower", "--conf=/flowerconfig.py"]
