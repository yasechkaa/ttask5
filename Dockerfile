FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY app/ .

# Запускаем через Gunicorn, указывая на файл wsgi и объект app внутри него
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]