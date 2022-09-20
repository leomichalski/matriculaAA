ARG BASE_CONTAINER=python:3.8-buster
FROM $BASE_CONTAINER

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN python -m pip install --no-cache-dir --default-timeout=15000 -r /tmp/requirements.txt

WORKDIR /src
COPY . .

RUN chmod +x ./start.sh
CMD ["./start.sh"]
