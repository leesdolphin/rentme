FROM rentme-py-base

ENV DJANGO_SETTINGS_MODULE=rentme.settings
RUN /venv/bin/pip3 install uwsgi && \
    echo '. /venv/bin/activate; set -ex' > /post-install.sh && \
    echo 'django-admin collectstatic --no-input < /dev/null' >> /post-install.sh && \
    echo 'django-admin migrate < /dev/null' >> /post-install.sh && \
    chmod +x /post-install.sh

COPY docker-utils/django.uwsgi.ini /django.uwsgi.ini

EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=1s --retries=20 CMD curl --silent --fail http://localhost:8000/api/healthcheck || exit 1
CMD ["uwsgi", "/django.uwsgi.ini"]
