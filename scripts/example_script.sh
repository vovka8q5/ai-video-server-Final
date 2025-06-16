#!/bin/bash

# Установка зависимостей
echo "Установка зависимостей..."
pip install -r requirements.txt

# Создание директорий
echo "Создание директорий..."
mkdir -p videos faces

# Загрузка примера изображения лица
echo "Загрузка примера изображения лица..."
wget -O faces/source_face.jpg https://example.com/source_face.jpg 
wget -O faces/target_face.jpg https://example.com/target_face.jpg 

# Загрузка примера музыки
echo "Загрузка примера музыки..."
wget -O music.mp3 https://example.com/music.mp3 

# Запуск основного скрипта
echo "Запуск основного скрипта..."
python src/main.py
