FROM python:3.9-alpine

LABEL AUTHOR="Amir Rezazadeh"

ENV PYTHONUNBUFFERED=1
ENV DOCKER_BUILDKIT=1


ENV PATH="/scripts:${PATH}"

RUN apk  \
    --repositories-file http://repo.iut.ac.ir/repo/alpine/v3.13/main/ \
    -X http://repo.iut.ac.ir/repo/alpine/v3.13/main/ \
    -X http://repo.iut.ac.ir/repo/alpine/v3.13/community/  \
    add postgresql-client jpeg-dev gcc libc-dev \
    linux-headers postgresql-dev musl-dev zlib zlib-dev

COPY ./requirements.txt /requirements.txt

RUN --mount=type=cache,target=/root/.cache \
    pip install -r /requirements.txt


RUN mkdir /app
COPY ./app /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]