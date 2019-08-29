FROM python:3.7-alpine

ADD requirements/ /requirements/
RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
        gcc \
        g++ \
        make \
        libc-dev \
        musl-dev \
        linux-headers \
        pcre-dev \
        postgresql-dev \
        libjpeg-turbo-dev \
        zlib-dev \
        expat-dev \
        git \
    && pyvenv /venv \
    && /venv/bin/pip install -U pip \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "/venv/bin/pip install -r /requirements/requirements.txt" \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /venv \
            | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
            | sort -u \
            | xargs -r apk info --installed \
            | sort -u \
    )" \
    && apk add --virtual .python-rundeps $runDeps \
    && apk del .build-deps \
    && apk add libjpeg-turbo pcre
RUN apk add --no-cache postgresql-client
RUN mkdir /code/
WORKDIR /code/
ADD . /code/
EXPOSE 8002

ENV DJANGO_SETTINGS_MODULE=test_m.settings

ENV UWSGI_VIRTUALENV=/venv UWSGI_WSGI_FILE=/code/test_m/wsgi.py UWSGI_HTTP=:8002 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000

RUN DATABASE_URL=postgres://none /venv/bin/python manage.py collectstatic --noinput

ENTRYPOINT ["/code/docker-entrypoint.sh"]
CMD ["/venv/bin/uwsgi", "--http-auto-chunked", "--http-keepalive"]
