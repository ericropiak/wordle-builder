FROM python:3.8-alpine

COPY requirements.txt requirements.txt
RUN apk update && \
    apk add --virtual build-deps gcc musl-dev && \
    apk add postgresql-dev && \
    apk add g++ && \
    apk add npm && \
    rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN npm ci --prefix app/static/

ENV FLASK_ENV=prod

EXPOSE 5001
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5001", "--log-level", "INFO", "manage:app" ]
