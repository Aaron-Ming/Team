FROM registry.saintic.com/alpine-python:gcc
MAINTAINER Mr.tao <staugur@saintic.com>
ADD ./src /Team.Auth
WORKDIR /Team.Auth
RUN pip install Flask Flask-RESTful tornado gevent setproctitle && chmod +x Product.py
EXPOSE 10030
ENTRYPOINT ["/Team.Auth/Product.py"]
