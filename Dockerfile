FROM python:3
MAINTAINER diego.crispim@yahoo.com.br

RUN apt-get update

COPY . /app
RUN make /app

RUN echo #!/bin/bash >> /bin/authorize
RUN echo 'python3 /app/cli.py $*' >> /bin/authorize
RUN chmod +x /bin/authorize

RUN authorize -tests

CMD clear && /bin/bash
