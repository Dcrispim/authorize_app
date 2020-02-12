FROM python:3
MAINTAINER diego.crispim@yahoo.com.br

COPY . /app

RUN apt-get update && echo 'python3 /app/cli.py $*' >> /bin/authorize && chmod +x /bin/authorize && authorize -tests

CMD clear && /bin/bash
