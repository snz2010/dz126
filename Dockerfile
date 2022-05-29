FROM python:3.10-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./views ./views
COPY ./db ./db
COPY app.py .
COPY config.py .
COPY models.py .
COPY setup_db.py .
VOLUME ./db


CMD flask run -h 0.0.0.0 -p 80