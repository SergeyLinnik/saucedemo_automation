"""
Демонстрация использования метода send_keys с XPATH
Автоматизация входа на сайт Saucedemo.com
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time


def login_to_saucedemo_with_xpath() -> None:
    """
    Функция демонстрирует использование метода send_keys
    для ввода логина и пароля на сайте Saucedemo.com
    Поиск элементов выполняется с помощью XPATH
    """
    # Настройка и запуск браузера Firefox (многострочный комментарий вместо трех print)
    """
    ==================================================
    ЗАПУСК ТЕСТА С ИСПОЛЬЗОВАНИЕМ XPATH
    ==================================================
    """
    
    # Запуск браузера
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Открытие сайта
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)
    
    # Поиск элементов с помощью XPATH
    username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
    password_field = driver.find_element(By.XPATH, "//input[@id='password']")
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    
    # Ввод данных с помощью send_keys
    username_field.clear()
    password_field.clear()
    username_field.send_keys("standard_user")
    password_field.send_keys("secret_sauce")
    time.sleep(1)
    
    # Нажатие кнопки входа
    login_button.click()
    time.sleep(2)
    
    # ПРОВЕРКА ТЕСТА ЧЕРЕЗ assert (основное требование)
    # assert проверяет условие и прерывает выполнение при ошибке
    assert "inventory.html" in driver.current_url, \
        f"ОШИБКА: Вход не выполнен. Текущий URL: {driver.current_url}"
    
    # Если assert прошел - выводим успешный результат (только для информации)
    print(f"УСПЕХ: Вход выполнен. URL: {driver.current_url}")
    
    # Проверка количества товаров через assert
    items = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
    assert len(items) == 6, \
        f"ОШИБКА: Найдено {len(items)} товаров, ожидалось 6"
    
    print(f"УСПЕХ: Найдено {len(items)} товаров")
    
    # Завершение теста
    time.sleep(3)
    driver.quit()
    
    print("\nТЕСТ ПРОЙДЕН УСПЕШНО")


# Запуск теста
if __name__ == "__main__":
    login_to_saucedemo_with_xpath()