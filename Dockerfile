FROM python:3.8.12-slim as base

RUN mkdir /speakbuddy
WORKDIR /speakbuddy

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg -y
RUN pip install -r requirements.txt

CMD ["python", "api/api.py"]
