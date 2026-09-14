"""
Расширенный тест для Saucedemo с использованием класса
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time


class SaucedemoTest:
    """Класс для тестирования Saucedemo"""
    
    def __init__(self):
        """Инициализация драйвера"""
        service = Service(GeckoDriverManager().install())
        self.driver = webdriver.Firefox(service=service)
        self.driver.maximize_window()
    
    def login(self, username, password):
        """Метод для входа в систему"""
        self.driver.get("https://www.saucedemo.com/")
        self.driver.find_element(By.ID, "user-name").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "login-button").click()
        time.sleep(1)
    
    def check_inventory(self):
        """Проверка страницы товаров"""
        if "inventory" in self.driver.current_url:
            items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
            print(f"[OK] Найдено товаров: {len(items)}")
            return True
        return False
    
    def add_to_cart(self, item_name):
        """Добавление товара в корзину"""
        button_id = f"add-to-cart-{item_name.lower().replace(' ', '-')}"
        self.driver.find_element(By.ID, button_id).click()
        print(f"[OK] Добавлен товар: {item_name}")
    
    def close(self):
        """Закрытие браузера"""
        time.sleep(3)
        self.driver.quit()


# Запуск теста
if __name__ == "__main__":
    print("Запуск расширенного теста...")
    test = SaucedemoTest()
    test.login("standard_user", "secret_sauce")
    
    if test.check_inventory():
        test.add_to_cart("Sauce Labs Backpack")
        test.add_to_cart("Sauce Labs Bike Light")
    
    test.close()
    print("Тест завершен успешно")