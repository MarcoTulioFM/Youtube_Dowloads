FROM python:latest

WORKDIR /usr/src/app/

COPY . .

RUN pip install pytube

RUN pip install flask

RUN pip install -U flask-cors

CMD ["python3", "dowload_youtube.py"]