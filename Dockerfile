FROM python:3.6-slim-stretch

RUN mkdir /app
COPY app/ /app/
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000
CMD python ./api.py
