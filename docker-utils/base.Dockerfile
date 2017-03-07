FROM python:3.5

ENV PYTHONUNBUFFERED 1

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user && mkdir /venv && chown -R user:user /venv && chmod ug+rw /venv
WORKDIR /home/user

RUN pip3 install dumb-init django celery aiohttp psycopg2 virtualenv

ADD ./rentme-startup.sh /

ENTRYPOINT ["/usr/local/bin/dumb-init", "/rentme-startup.sh"]

VOLUME ["/venv"]
