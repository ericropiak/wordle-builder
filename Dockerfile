# Dockerfile is used for product deployments (not actually used by OpenShift :( )
FROM python:3.8

COPY requirements.txt requirements.txt
# RUN apt-get update && \
#     apt-get add --virtual build-deps gcc musl-dev && \
#     apt-get add postgresql-dev && \
#     apt-get -y install npm && \
#     rm -rf /var/cache/apk/*
RUN  yum -y install nodejs

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN pwd
sddfsd
RUN npm ci --prefix ~/app/static

ENV FLASK_ENV=prod

EXPOSE 5001
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5001", "--log-level", "INFO", "manage:app" ]
