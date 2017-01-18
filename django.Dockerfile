FROM rentme-py-base

ENV DJANGO_SETTINGS_MODULE=rentme.settings
RUN pip install uwsgi && \
    echo 'django-admin collectstatic' > post-install.sh && \
    chmod +x post-install.sh

ADD docker-utils/django.uwsgi.ini /django.uwsgi.ini

EXPOSE 8000

CMD ["uwsgi", "/django.uwsgi.ini"]
