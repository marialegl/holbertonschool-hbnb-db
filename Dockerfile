FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

ENV PORT 5000

VOLUME ["/app/data"]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]