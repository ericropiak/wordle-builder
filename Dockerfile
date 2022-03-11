# Dockerfile is used for product deployments (not actually used by OpenShift :( )
FROM python:3.8

COPY requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    rm -rf /var/cache/apk/*
RUN apt-get update && apt-get -y install npm

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN pwd
sddfsd
RUN npm ci --prefix ~/app/static

ENV FLASK_ENV=prod

EXPOSE 5001
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5001", "--log-level", "INFO", "manage:app" ]
