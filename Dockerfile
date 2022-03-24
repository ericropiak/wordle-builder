FROM rhscl/python-38-rhel7

COPY requirements.txt requirements.txt
USER root
RUN --disableplugin=subscription-manager yum update
RUN yum --disableplugin=subscription-manager install g++
RUN yum --disableplugin=subscription-manager install -y npm
RUN yum --disableplugin=subscription-manager install -y postgresql-client

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

RUN npm ci --prefix app/static/
# Allow flask asset builder to modify this directory
RUN chmod -R 777 app/static/

ENV FLASK_ENV=prod

EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--chdir",  "app", "--log-level", "INFO", "--worker-class",  "eventlet",  "-w", "1", "wsgi:application" ]
