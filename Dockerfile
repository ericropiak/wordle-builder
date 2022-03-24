FROM ubi8/python-38
# RUN yum --disableplugin=subscription-manager update && yum install -y python3 && yum install g++ && yum install -y npm && yum install -y postgresql-client

COPY requirements.txt requirements.txt
# USER root
RUN yum update --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos -y && rm -rf /var/cache/yum
# RUN yum install --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos python3 -y && rm -rf /var/cache/yum
RUN yum install --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos npm -y && rm -rf /var/cache/yum
RUN yum install --disablerepo=* --enablerepo=ubi-8-appstream --enablerepo=ubi-8-baseos gcc-c++ -y && rm -rf /var/cache/yum

# RUN yum --disableplugin=subscription-manager install g++
# RUN yum --disableplugin=subscription-manager install -y npm
# RUN yum --disableplugin=subscription-manager install -y postgresql-client

RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

RUN npm ci --prefix app/static/
# Allow flask asset builder to modify this directory
RUN chmod -R 777 app/static/

ENV FLASK_ENV=prod

EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8080", "--chdir",  "app", "--log-level", "INFO", "--worker-class",  "eventlet",  "-w", "1", "wsgi:application" ]
