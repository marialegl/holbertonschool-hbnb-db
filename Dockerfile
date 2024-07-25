FROM python:3.9-alpine

WORKDIR /app

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

COPY . /app

EXPOSE $PORT

ENV PORT 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]