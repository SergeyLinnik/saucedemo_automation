"""
Автоматизация авторизации на сайте Saucedemo.com
Использование метода .click() для нажатия кнопки входа
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_with_click_method() -> None:
    """
    Функция демонстрирует использование метода .click()
    для авторизации на сайте Saucedemo.com
    """
    """
    ==================================================
    ЗАПУСК ТЕСТА АВТОРИЗАЦИИ С ИСПОЛЬЗОВАНИЕМ .click()
    ==================================================
    """
    
    # Настройка и запуск браузера Firefox
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Открытие сайта
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)
    
    # Поиск элементов на странице с помощью XPATH
    # Поле для ввода логина
    username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
    
    # Поле для ввода пароля
    password_field = driver.find_element(By.XPATH, "//input[@id='password']")
    
    # Кнопка входа (на которую будем нажимать .click())
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    
    # Ввод логина с помощью send_keys
    username_field.clear()
    username_field.send_keys("standard_user")
    
    # Ввод пароля с помощью send_keys
    password_field.clear()
    password_field.send_keys("secret_sauce")
    
    time.sleep(1)
    
    # ============================================
    # ИСПОЛЬЗОВАНИЕ МЕТОДА .click() ДЛЯ АВТОРИЗАЦИИ
    # ============================================
    # Метод .click() имитирует нажатие левой кнопкой мыши на элемент
    # В данном случае - нажатие кнопки "Login" для отправки формы
    print("Выполнение авторизации через .click()...")
    login_button.click()
    
    # Ожидание загрузки страницы после клика
    time.sleep(2)
    
    # ============================================
    # ПРОВЕРКА РЕЗУЛЬТАТА АВТОРИЗАЦИИ ЧЕРЕЗ assert
    # ============================================
    
    # Проверка URL после авторизации
    assert "inventory.html" in driver.current_url, \
        f"ОШИБКА: Авторизация не выполнена. Текущий URL: {driver.current_url}"
    
    print(f"УСПЕХ: Авторизация выполнена. URL: {driver.current_url}")
    
    # Проверка количества товаров на странице
    items = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
    assert len(items) == 6, \
        f"ОШИБКА: Найдено {len(items)} товаров, ожидалось 6"
    
    print(f"УСПЕХ: Найдено {len(items)} товаров")
    
    # Завершение теста
    print("\nМетод .click() успешно отработал. Браузер закроется через 3 секунды...")
    time.sleep(3)
    driver.quit()
    
    print("\nТЕСТ АВТОРИЗАЦИИ ПРОЙДЕН УСПЕШНО")


def alternative_click_examples() -> None:
    """
    Дополнительная функция с примерами использования метода .click()
    для различных элементов на странице
    """
    """
    ==================================================
    ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ МЕТОДА .click()
    ==================================================
    """
    
    print("""
    Примеры использования метода .click() в Selenium:
    
    1. Нажатие на кнопку:
       button.click()
    
    2. Нажатие на ссылку:
       link.click()
    
    3. Нажатие на чекбокс:
       checkbox.click()
    
    4. Нажатие на радиокнопку:
       radio_button.click()
    
    5. Нажатие на элемент меню:
       menu_item.click()
    
    Особенности метода .click():
    - Имитирует реальное действие пользователя
    - Ожидает, что элемент будет видим и доступен для клика
    - Выбрасывает исключение, если элемент не интерактивен
    - Для лучшей надежности можно использовать WebDriverWait
    """)
    
    print("Пример с WebDriverWait для надежного клика:")
    print("""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Ожидание, пока кнопка станет кликабельной, затем клик
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    button.click()
    """)


def login_with_explicit_wait() -> None:
    """
    Альтернативная версия с явным ожиданием (WebDriverWait)
    Более надежный способ авторизации
    """
    """
    ==================================================
    АВТОРИЗАЦИЯ С ЯВНЫМ ОЖИДАНИЕМ (WebDriverWait)
    ==================================================
    """
    
    # Настройка и запуск браузера Firefox
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Открытие сайта
    driver.get("https://www.saucedemo.com/")
    
    # Явное ожидание загрузки элементов
    wait = WebDriverWait(driver, 10)
    
    # Ожидание поля ввода логина
    username_field = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']"))
    )
    username_field.send_keys("standard_user")
    
    # Ожидание поля ввода пароля
    password_field = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='password']"))
    )
    password_field.send_keys("secret_sauce")
    
    # Ожидание, когда кнопка станет кликабельной, и клик
    login_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='login-button']"))
    )
    login_button.click()
    
    # Проверка результата
    wait.until(EC.url_contains("inventory.html"))
    assert "inventory.html" in driver.current_url
    
    print("УСПЕХ: Авторизация с явным ожиданием выполнена")
    
    time.sleep(2)
    driver.quit()


# Запуск основной функции
if __name__ == "__main__":
    # Основной тест с .click()
    login_with_click_method()
    
    # Вывод примеров (раскомментируйте при необходимости)
    # alternative_click_examples()
    # login_with_explicit_wait()