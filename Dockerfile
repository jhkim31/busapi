FROM python

WORKDIR /app

COPY ./BusApi .

RUN pip install flask 
RUN pip install requests
RUN pip install xmltodict

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install vim -y

