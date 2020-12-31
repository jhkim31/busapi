FROM python

WORKDIR /app

COPY ./BusApi .

RUN pip install flask
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y

