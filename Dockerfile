FROM python:3.9.7
RUN mkdir /fampay
ADD . /fampay/
WORKDIR /fampay
RUN pip install -r requirements.txt