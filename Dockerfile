FROM python:3.7-alpine

RUN apk add --no-cache --virtual .build-deps gcc postgresql-dev musl-dev python3-dev curl libressl-dev libffi-dev

RUN apk add libpq
RUN pip install "poetry==1.0.0"

RUN mkdir /app 
WORKDIR /app

COPY pyproject.toml /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

CMD gunicorn -w 1 -b "0.0.0.0:9080" -t 300 src.falcon_app:app
# ENV FLASK_APP=src/flask_app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
# CMD flask run --host=0.0.0.0 --port=80