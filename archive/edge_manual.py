"""
Запуск Microsoft Edge с ручным указанием драйвера
Используется уже скачанный файл msedgedriver.exe
"""

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import os

# Путь к скачанному драйверу (файл уже есть в папке)
current_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_dir, "msedgedriver.exe")

print("=" * 50)
print("ЗАПУСК MICROSOFT EDGE")
print("=" * 50)
print(f"Путь к драйверу: {driver_path}")
print(f"Файл существует: {os.path.exists(driver_path)}")

try:
    # Проверка наличия драйвера
    if not os.path.exists(driver_path):
        print("ОШИБКА: Файл msedgedriver.exe не найден!")
        exit(1)
    
    # Настройка Edge
    print("1. Настройка Edge...")
    edge_options = Options()
    edge_options.add_argument("--start-maximized")
    
    # Запуск с указанием пути к драйверу
    print("2. Запуск Edge драйвера...")
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    print("3. Edge успешно запущен")
    
    # Открытие сайта
    print("4. Открытие сайта...")
    driver.get("https://www.saucedemo.com/")
    
    time.sleep(2)
    print(f"5. Текущий URL: {driver.current_url}")
    print("6. УСПЕХ: Edge загрузил сайт")
    
    # Можно добавить вход в систему
    print("\n7. Выполняем вход в систему...")
    username = driver.find_element("id", "user-name")
    password = driver.find_element("id", "password")
    login_btn = driver.find_element("id", "login-button")
    
    username.send_keys("standard_user")
    password.send_keys("secret_sauce")
    login_btn.click()
    
    time.sleep(2)
    print(f"8. URL после входа: {driver.current_url}")
    
    if "inventory" in driver.current_url:
        print("9. УСПЕХ: Вход выполнен успешно")
        
        # Подсчет товаров
        items = driver.find_elements("class name", "inventory_item")
        print(f"10. Найдено товаров: {len(items)}")
    
    print("\nБраузер закроется через 10 секунд...")
    time.sleep(10)
    
    driver.quit()
    print("Edge закрыт")
    print("=" * 50)
    print("ТЕСТ УСПЕШНО ЗАВЕРШЕН")
    print("=" * 50)
    
except Exception as e:
    print(f"ОШИБКА: {e}")
    print("\nВозможные решения:")
    print("1. Проверьте, что версия Edge соответствует версии драйвера")
    print("2. Обновите Edge до последней версии")
    print("3. Скачайте новую версию драйвера с сайта Microsoft")