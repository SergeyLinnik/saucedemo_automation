"""
Демонстрация использования метода send_keys для автоматизации входа на Saucedemo
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
from typing import None


def login_to_saucedemo() -> None:
    """
    Функция демонстрирует использование метода send_keys
    для ввода логина и пароля на сайте Saucedemo.com
    """
    # Настройка и запуск браузера Firefox
    print("Запуск браузера Firefox...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Открытие сайта
    driver.get("https://www.saucedemo.com/")
    time.sleep(1)
    
    # Поиск элементов на странице
    # Находим поле для ввода логина по ID
    username_field = driver.find_element(By.ID, "user-name")
    
    # Находим поле для ввода пароля по ID
    password_field = driver.find_element(By.ID, "password")
    
    # Находим кнопку входа по ID
    login_button = driver.find_element(By.ID, "login-button")
    
    # Использование метода send_keys для ввода значений
    # Метод send_keys имитирует ввод текста с клавиатуры
    username_field.send_keys("standard_user")  # Ввод логина
    password_field.send_keys("secret_sauce")   # Ввод пароля
    
    # Нажатие кнопки входа
    login_button.click()
    
    # Ожидание загрузки следующей страницы
    time.sleep(2)
    
    # Проверка успешного входа
    if "inventory.html" in driver.current_url:
        print("Успешный вход! Использован метод send_keys.")
        print(f"Текущий URL: {driver.current_url}")
    else:
        print("Ошибка входа")
    
    # Закрытие браузера
    print("Браузер закроется через 3 секунды...")
    time.sleep(3)
    driver.quit()


# Запуск функции
if __name__ == "__main__":
    login_to_saucedemo()