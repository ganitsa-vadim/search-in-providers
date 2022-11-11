FROM python:3.10

RUN apt-get update
RUN apt-get -y install make

COPY Makefile Pipfile Pipfile.lock /app/
WORKDIR /app

RUN make setup

COPY . /app
EXPOSE 9000
CMD make run
