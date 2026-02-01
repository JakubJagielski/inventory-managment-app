FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src src

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SQLITE_DB_PATH=/app/data/db.sqlite3 
ENV PYTHONPATH=src

EXPOSE 8000

CMD ["sh", "-c", "python src/manage.py makemigrations inventory && python src/manage.py migrate && python src/manage.py runserver 0.0.0.0:8000"]
