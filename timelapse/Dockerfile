FROM ubuntu:latest

RUN apt-get update
RUN apt-get install python3-pip python3-dev build-essential -y
RUN apt-get install imagemagick -y
RUN apt-get install unzip -y
RUN apt-get install ffmpeg -y
RUN apt-get install software-properties-common -y
RUN add-apt-repository ppa:dhor/myway
RUN apt-get install dcraw -y
VOLUME /tmp

COPY . /app
ENV HOME=/app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENV FLASK_APP=app.py

EXPOSE 8084

ENTRYPOINT ["gunicorn","-b","0.0.0.0:8084","-w","4","app:app"]

