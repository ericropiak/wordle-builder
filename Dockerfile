FROM python:3.8

COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get install postgresql-dev && \
    apt-get install g++ && \
    apt-get install npm &&

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN npm ci --prefix app/static/

ENV FLASK_ENV=prod

EXPOSE 5001
ENTRYPOINT [ "gunicorn", "--chdir",  "app", "--log-level", "INFO", "main:app" ]
