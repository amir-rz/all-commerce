FROM python:3.9-alpine

LABEL AUTHOR="Amir Rezazadeh"

ENV PYTHONUNBUFFERED 1

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk  \
    -X http://dl-4.alpinelinux.org/alpine/v3.13/main \
    -X http://dl-4.alpinelinux.org/alpine/v3.13/community  \
    add --update --no-cache postgresql-client jpeg-dev
RUN apk  \
    -X http://dl-4.alpinelinux.org/alpine/v3.13/main \
    -X http://dl-4.alpinelinux.org/alpine/v3.13/community  \
    add --update --no-cache --virtual .tmp \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
    
RUN pip install -r /requirements.txt
RUN apk del .tmp

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