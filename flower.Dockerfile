FROM rentme-py-base

RUN pip3 install flower && \
    mkdir -p /flower-db && \
    chmod a+rw /flower-db

COPY docker-utils/flowerconfig.py /flowerconfig.py

EXPOSE 5555

HEALTHCHECK --interval=5s --timeout=1s --retries=20 CMD curl --silent --fail http://localhost:5555/ || exit 1
CMD ["python3", "-m", "celery", "-E", "-A", "rentme.data.importer.celery", "flower", "--conf=/flowerconfig.py"]

COPY ["trademe", "rentme", "aioutils", "requirements.txt", "setup.py", "setup.cfg", "manage.py", "/code/"]
RUN /venv/bin/pip install -e /code
