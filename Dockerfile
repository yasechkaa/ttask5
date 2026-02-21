FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости из подпапки app
COPY app/requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое папки app в контейнер
COPY app/ .

# Запускаем через gunicorn (порт 8000, как в твоих логах)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]
