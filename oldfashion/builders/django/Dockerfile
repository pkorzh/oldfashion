FROM ubuntu:14.04

RUN apt-get update

RUN apt-get install -y build-essential python python-dev python-pip python-setuptools nginx supervisor

RUN pip install uwsgi

ADD . /usr/src/app

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default

RUN ln -s /usr/src/app/nginx-app.conf /etc/nginx/sites-enabled/
RUN ln -s /usr/src/app/supervisor-app.conf /etc/supervisor/conf.d/

RUN pip install -r /usr/src/app/requirements.txt

EXPOSE 80
CMD ["/usr/bin/supervisord"]