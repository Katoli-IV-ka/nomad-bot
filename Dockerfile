# Используем минимальный образ с Python
FROM python:3.9-slim

# Устанавливаем необходимые системные пакеты
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости для Python
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Открываем порт (если нужно)
EXPOSE 8000

# Запускаем приложение (или команду, чтобы оно стартовало)
CMD ["python", "your_app.py"]  # Замените на нужную команду для вашего проекта
