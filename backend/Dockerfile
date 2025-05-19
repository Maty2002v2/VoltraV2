FROM python:3.11-slim

WORKDIR /code

# zainstaluj kompilator i zależności do psycopg2
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# requirements.txt powinien być w /backend/requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# skopiuj cały katalog backend do /code
COPY . .

# wskaż Django, gdzie ustawiać settings, i expose port
ENV DJANGO_SETTINGS_MODULE=app.settings
EXPOSE 8000
RUN python manage.py collectstatic --noinput

# w Dockerfile.backend, na końcu:
CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000"]
