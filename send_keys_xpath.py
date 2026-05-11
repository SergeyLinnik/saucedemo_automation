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
    # Настройка и запуск браузера Firefox
    print("=" * 50)
    print("ЗАПУСК ТЕСТА С ИСПОЛЬЗОВАНИЕМ XPATH")
    print("=" * 50)
    
    print("\n1. Запуск браузера Firefox...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Открытие сайта
    print("2. Открытие сайта...")
    driver.get("https://www.saucedemo.com/")
    time.sleep(2)
    
    # ============================================
    # ПОИСК ЭЛЕМЕНТОВ С ПОМОЩЬЮ XPATH
    # ============================================
    
    # Способ 1: XPATH по атрибуту id
    # Находим поле для ввода логина по атрибуту id
    print("\n3. Поиск элементов с помощью XPATH...")
    
    # XPATH: ищем элемент с id='user-name'
    username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
    print("   - Поле логина найдено по XPATH: //input[@id='user-name']")
    
    # XPATH: ищем элемент с id='password'
    password_field = driver.find_element(By.XPATH, "//input[@id='password']")
    print("   - Поле пароля найдено по XPATH: //input[@id='password']")
    
    # XPATH: ищем кнопку с id='login-button'
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    print("   - Кнопка входа найдена по XPATH: //input[@id='login-button']")
    
    # ============================================
    # ВВОД ДАННЫХ С ПОМОЩЬЮ send_keys
    # ============================================
    
    print("\n4. Ввод данных с помощью send_keys...")
    
    # Очистка полей (на всякий случай)
    username_field.clear()
    password_field.clear()
    
    # Ввод логина
    username_field.send_keys("standard_user")
    print("   - Логин введен: standard_user")
    
    # Ввод пароля
    password_field.send_keys("secret_sauce")
    print("   - Пароль введен: secret_sauce")
    
    # Небольшая пауза для визуального контроля
    time.sleep(1)
    
    # Нажатие кнопки входа
    print("\n5. Нажатие кнопки входа...")
    login_button.click()
    
    # Ожидание загрузки следующей страницы
    time.sleep(2)
    
    # ============================================
    # ПРОВЕРКА РЕЗУЛЬТАТА
    # ============================================
    
    print("\n6. Проверка результата...")
    if "inventory.html" in driver.current_url:
        print("   УСПЕХ! Вход выполнен успешно.")
        print(f"   Текущий URL: {driver.current_url}")
        
        # Подсчет товаров на странице (тоже через XPATH)
        items = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
        print(f"   Найдено товаров: {len(items)}")
    else:
        print(f"   ОШИБКА! Текущий URL: {driver.current_url}")
    
    # Завершение теста
    print("\n7. Завершение теста...")
    print("   Браузер закроется через 5 секунд...")
    time.sleep(5)
    driver.quit()
    
    print("\n" + "=" * 50)
    print("ТЕСТ ЗАВЕРШЕН")
    print("=" * 50)


def alternative_xpath_examples() -> None:
    """
    Дополнительная функция с примерами различных XPATH
    для поиска элементов на странице
    """
    print("\n" + "=" * 50)
    print("ПРИМЕРЫ РАЗЛИЧНЫХ XPATH ВЫРАЖЕНИЙ")
    print("=" * 50)
    
    print("""
    Для поиска поля логина можно использовать разные XPATH:
    
    1. По атрибуту id:
       //input[@id='user-name']
    
    2. По атрибуту placeholder:
       //input[@placeholder='Username']
    
    3. По атрибуту name:
       //input[@name='user-name']
    
    4. По атрибуту class:
       //input[@class='form_input']
    
    5. Частичное совпадение по атрибуту:
       //input[contains(@id, 'user')]
    
    6. По тексту метки (если есть):
       //label[text()='Username']/following-sibling::input
    
    7. По позиции (первый input):
       (//input)[1]
    
    Рекомендуется использовать наиболее специфичный XPATH
    для надежного поиска элемента.
    """)


# Запуск основной функции
if __name__ == "__main__":
    login_to_saucedemo_with_xpath()
    alternative_xpath_examples()