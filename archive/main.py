"""
Проект автоматизации тестирования для Saucedemo.com
Использует Selenium WebDriver (Firefox) для открытия браузера
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import time


def open_saucedemo() -> None:
    """
    Открывает браузер Firefox и переходит на сайт Saucedemo.com
    """
    print("Запуск автоматизации тестирования...")
    
    print("Настройка Firefox WebDriver...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    
    try:
        url = "https://www.saucedemo.com/"
        print(f"Открываем браузер и переходим на: {url}")
        driver.get(url)
        driver.maximize_window()
        driver.implicitly_wait(10)
        
        print(f"Текущий URL: {driver.current_url}")
        print(f"Заголовок страницы: {driver.title}")
        
        print("\nПоиск элементов на странице...")
        username_field = driver.find_element(By.ID, "user-name")
        password_field = driver.find_element(By.ID, "password")
        login_button = driver.find_element(By.ID, "login-button")
        print("Все элементы найдены")
        
        print("\nВвод данных для входа...")
        username_field.clear()
        password_field.clear()
        
        username_field.send_keys("standard_user")
        print("Введен Username: standard_user")
        
        password_field.send_keys("secret_sauce")
        print("Введен Password: secret_sauce")
        
        time.sleep(1)
        login_button.click()
        print("Нажата кнопка Login...")
        
        WebDriverWait(driver, 10).until(
            EC.url_contains("inventory.html")
        )
        
        print(f"Успешный вход! Текущий URL: {driver.current_url}")
        print("Открыта страница инвентаря с товарами")
        
        print("\nБраузер останется открытым на 5 секунд...")
        time.sleep(5)
        
    except Exception as error:
        print(f"Произошла ошибка: {type(error).__name__}")
        print(f"Детали ошибки: {error}")
    
    finally:
        print("\nЗакрытие браузера...")
        time.sleep(2)
        driver.quit()
        print("Браузер закрыт. Тест завершен.")


if __name__ == "__main__":
    open_saucedemo()