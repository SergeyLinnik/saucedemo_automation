"""
Упрощенный негативный тест авторизации
По одному тесту для проверки работоспособности
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time


def test_single_negative() -> None:
    """
    Простой негативный тест с одним сценарием
    """
    print("Запуск браузера...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    try:
        # Открытие сайта
        print("Открытие сайта...")
        driver.get("https://www.saucedemo.com/")
        time.sleep(2)
        
        # Ввод неверных данных
        print("Ввод неверного пароля...")
        username = driver.find_element(By.XPATH, "//input[@id='user-name']")
        password = driver.find_element(By.XPATH, "//input[@id='password']")
        
        username.send_keys("standard_user")
        password.send_keys("wrong_password")
        
        # Нажатие кнопки
        print("Нажатие кнопки входа...")
        login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
        login_button.click()
        
        time.sleep(2)
        
        # Проверка ошибки
        print("Проверка сообщения об ошибке...")
        error_container = driver.find_element(By.XPATH, "//div[@class='error-message-container error']")
        assert error_container.is_displayed(), "Ошибка не отображается"
        print("✅ Сообщение об ошибке отображается")
        
        # Получение текста ошибки
        error_text = error_container.find_element(By.XPATH, ".//h3").text
        print(f"📝 Текст ошибки: {error_text}")
        
        # Закрытие ошибки
        print("Закрытие сообщения об ошибке...")
        close_button = driver.find_element(By.XPATH, "//button[@class='error-button']")
        close_button.click()
        time.sleep(1)
        
        # Проверка, что ошибка закрылась
        try:
            driver.find_element(By.XPATH, "//div[@class='error-message-container error']")
            print("❌ Ошибка все еще отображается")
        except:
            print("✅ Ошибка успешно закрыта")
        
        print("\n✅ ТЕСТ ПРОЙДЕН")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    finally:
        time.sleep(2)
        driver.quit()


if __name__ == "__main__":
    test_single_negative()