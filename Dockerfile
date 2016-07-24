FROM registry.saintic.com/alpine-python:gcc
MAINTAINER Mr.tao <staugur@saintic.com>
ADD ./src /Team.Front
WORKDIR /Team.Front
RUN pip install Flask tornado gevent setproctitle redis redis-py-cluster && chmod +x Product.py
EXPOSE 10050
ENTRYPOINT ["/Team.Front/Product.py"]
