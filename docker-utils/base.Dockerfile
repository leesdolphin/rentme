FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS all

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user && mkdir /venv && chown -R user:user /venv && chmod ug+rw /venv
WORKDIR /home/user

RUN pip3 install --upgrade pip setuptools wheel \
    && pip3 install --upgrade dumb-init virtualenv \
    && python3 -m virtualenv --python=python3 --system-site-packages /venv \
    && /venv/bin/pip3 install --upgrade pip setuptools wheel \
    && /venv/bin/pip3 install --upgrade django celery aiohttp psycopg2

ENTRYPOINT ["/usr/local/bin/dumb-init", "/rentme-startup.sh"]

COPY ["docker-requirements.txt", "/"]

RUN /venv/bin/pip3 install -r /docker-requirements.txt

COPY ["./rentme-startup.sh", "/"]
