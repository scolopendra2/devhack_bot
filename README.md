# Бейджи статус пайплайна CI/CD
[![pipeline Status](https://github.com/scolopendra2/devhack_bot/actions/workflows/main.yml/badge.svg)](https://github.com/scolopendra2/dgtu_bot/actions/workflows/main.yml)

# Python
[![Python Version](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/downloads/release/python-3100/)

# Клонирование репозитория
git clone https://github.com/scolopendra2/devhack_bot

# Установка и запуск виртуального окружения
python -m venv venv

venv/Scripts/activate

# Установка зависимостей
pip install -r requirements/prod.txt

# Подстановка секретных переменных в окружение
BOT_TOKEN - токен вашего бота
MYSQL_DBNAME - название базы данных
MYSQL_USER - имя пользователя
MYSQL_PASSWORD - пароль
MYSQL_HOST - хост
MYSQL_PORT - порт

# Запуск бота
python app.py