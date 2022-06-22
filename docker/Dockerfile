ARG BASE_CONTAINER=python:3.8-buster
FROM $BASE_CONTAINER

COPY docker/requirements.txt /tmp/
RUN pip install --default-timeout=15000 --requirement /tmp/requirements.txt
