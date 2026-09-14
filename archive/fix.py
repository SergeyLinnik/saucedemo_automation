import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

print("=== Диагностика проблемы с ChromeDriver ===\n")

# Проверяем версию Python
print(f"Версия Python: {os.sys.version}")

# Способ 1: Попробуем простой запуск
try:
    print("\n1. Пробуем простой запуск webdriver.Chrome()...")
    driver = webdriver.Chrome()
    print("Простой запуск сработал!")
    driver.get("https://www.saucedemo.com/")
    print("Сайт открылся!")
    time.sleep(3)
    driver.quit()
except Exception as e:
    print(f"Ошибка: {e}")
    print("Проблема с автоматическим поиском драйвера")

# Способ 2: Информация о системе
print("\n2. Информация о системе:")
print(f"   Путь к Python: {os.sys.executable}")
print(f"   Рабочая директория: {os.getcwd()}")

print("\n=== Рекомендации ===")
print("Если ничего не работает, установите Firefox:")
print("1. Скачайте Firefox с https://www.mozilla.org/ru/firefox/")
print("2. Установите его")
print("3. Затем запустите: pip install webdriver-manager")