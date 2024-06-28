FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV PORT 8000

VOLUME ["/app/data"]

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT} api.app:app"]