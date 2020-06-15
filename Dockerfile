FROM python:latest

WORKDIR /sentry

COPY . /sentry

USER root

RUN pip install .

CMD [ "sentry" ]
