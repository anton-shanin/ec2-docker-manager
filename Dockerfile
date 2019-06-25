FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3 && \
    pip3 install --upgrade pip setuptools

COPY . /app

WORKDIR /app

RUN pip3 install -r ./requirements.txt

RUN python3 setup.py develop

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]