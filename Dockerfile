# Используем официальный образ Python с минимальной сборкой
FROM python:3.11-slim

# Установим рабочую директорию
WORKDIR /app

# Установим только необходимые пакеты
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей и устанавливаем зависимости
COPY nomad-bot-main/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код проекта
COPY nomad-bot-main/ .

# По необходимости можно добавить переменные окружения или порты

# Команда для запуска бота
CMD ["python", "main.py"]
