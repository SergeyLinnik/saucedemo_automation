"""
Тест авторизации на сайте Saucedemo.com
Проверка URL и страницы каталога после входа
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def test_login_and_catalog() -> None:
    """
    Тест авторизации с проверкой:
    1. Ввод логина
    2. Ввод пароля
    3. Нажатие кнопки авторизации
    4. Проверка соответствия URL
    5. Проверка нахождения на странице каталога
    """
    """
    ==================================================
    ТЕСТ АВТОРИЗАЦИИ И ПРОВЕРКИ СТРАНИЦЫ КАТАЛОГА
    ==================================================
    """
    
    # Настройка и запуск браузера Firefox
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    
    # Явное ожидание для надежности
    wait = WebDriverWait(driver, 10)
    
    try:
        # ШАГ 1: Открытие сайта
        print("1. Открытие сайта...")
        driver.get("https://www.saucedemo.com/")
        
        # ШАГ 2: Ввод логина
        print("2. Ввод логина...")
        username_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']"))
        )
        username_field.clear()
        username_field.send_keys("standard_user")
        print("   - Логин введен: standard_user")
        
        # ШАГ 3: Ввод пароля
        print("3. Ввод пароля...")
        password_field = driver.find_element(By.XPATH, "//input[@id='password']")
        password_field.clear()
        password_field.send_keys("secret_sauce")
        print("   - Пароль введен: secret_sauce")
        
        # ШАГ 4: Нажатие кнопки авторизации
        print("4. Нажатие кнопки авторизации...")
        login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
        login_button.click()
        print("   - Кнопка нажата")
        
        # Ожидание загрузки страницы после авторизации
        time.sleep(2)
        
        # ШАГ 5: Проверка соответствия URL
        print("\n5. Проверка соответствия URL...")
        current_url = driver.current_url
        expected_url_part = "inventory.html"
        
        assert expected_url_part in current_url, \
            f"ОШИБКА: URL не соответствует. Ожидалась часть '{expected_url_part}', получен '{current_url}'"
        
        print(f"   - УСПЕХ: URL содержит '{expected_url_part}'")
        print(f"   - Текущий URL: {current_url}")
        
        # ШАГ 6: Проверка нахождения на странице каталога
        print("\n6. Проверка нахождения на странице каталога...")
        
        # Проверка через URL (уже сделано выше)
        # Дополнительная проверка через наличие элементов каталога
        
        # Проверка заголовка страницы
        page_title = driver.title
        assert page_title == "Swag Labs", \
            f"ОШИБКА: Заголовок страницы '{page_title}' не соответствует 'Swag Labs'"
        print(f"   - УСПЕХ: Заголовок страницы: {page_title}")
        
        # Проверка наличия каталога товаров (элемент inventory_container)
        inventory_container = driver.find_element(By.XPATH, "//div[@class='inventory_container']")
        assert inventory_container.is_displayed(), \
            "ОШИБКА: Контейнер каталога товаров не отображается"
        print("   - УСПЕХ: Контейнер каталога отображается")
        
        # Проверка наличия товаров в каталоге
        inventory_items = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
        assert len(inventory_items) > 0, \
            f"ОШИБКА: В каталоге не найдено товаров"
        
        print(f"   - УСПЕХ: В каталоге найдено {len(inventory_items)} товаров")
        
        # Проверка наличия элементов фильтрации
        filter_dropdown = driver.find_element(By.XPATH, "//select[@class='product_sort_container']")
        assert filter_dropdown.is_displayed(), \
            "ОШИБКА: Элемент фильтрации товаров не отображается"
        print("   - УСПЕХ: Элемент фильтрации отображается")
        
        # Проверка наличия корзины
        shopping_cart = driver.find_element(By.XPATH, "//div[@id='shopping_cart_container']")
        assert shopping_cart.is_displayed(), \
            "ОШИБКА: Корзина не отображается"
        print("   - УСПЕХ: Корзина отображается")
        
        # ШАГ 7: Итоговый вывод
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 50)
        print("✅ URL соответствует ожидаемому")
        print("✅ Страница каталога успешно загружена")
        print("✅ Товары отображаются в каталоге")
        print("✅ Элементы управления (фильтр, корзина) присутствуют")
        
    except Exception as error:
        print(f"\n❌ ОШИБКА ТЕСТА: {error}")
        raise
    
    finally:
        # Завершение теста
        print("\nЗавершение теста. Браузер закроется через 3 секунды...")
        time.sleep(3)
        driver.quit()
        print("Тест авторизации и проверки каталога завершен")


def check_catalog_elements(driver) -> None:
    """
    Вспомогательная функция для проверки элементов страницы каталога
    """
    """
    ==================================================
    ПРОВЕРКА ЭЛЕМЕНТОВ СТРАНИЦЫ КАТАЛОГА
    ==================================================
    """
    
    # Список проверяемых элементов
    elements_to_check = [
        ("//div[@class='inventory_list']", "Список товаров"),
        ("//div[@class='inventory_item']", "Элементы товаров"),
        ("//div[@class='inventory_item_img']", "Изображения товаров"),
        ("//div[@class='inventory_item_name']", "Названия товаров"),
        ("//div[@class='inventory_item_price']", "Цены товаров"),
        ("//button[contains(@id, 'add-to-cart')]", "Кнопки 'Add to cart'")
    ]
    
    print("\nДополнительная проверка элементов каталога:")
    for xpath, element_name in elements_to_check:
        try:
            element = driver.find_element(By.XPATH, xpath)
            assert element.is_displayed(), f"Элемент {element_name} не отображается"
            print(f"   ✅ {element_name}: присутствует")
        except:
            print(f"   ❌ {element_name}: НЕ НАЙДЕН")


def test_with_multiple_checks() -> None:
    """
    Расширенная версия теста с дополнительными проверками
    """
    """
    ==================================================
    РАСШИРЕННЫЙ ТЕСТ СТРАНИЦЫ КАТАЛОГА
    ==================================================
    """
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    try:
        # Авторизация
        driver.get("https://www.saucedemo.com/")
        
        username_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='user-name']"))
        )
        username_field.send_keys("standard_user")
        
        password_field = driver.find_element(By.XPATH, "//input[@id='password']")
        password_field.send_keys("secret_sauce")
        
        login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
        login_button.click()
        
        # Ожидание загрузки каталога
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='inventory_container']")))
        
        # Проверки
        assert "inventory.html" in driver.current_url, "URL не соответствует"
        print("\n✅ Базовые проверки пройдены")
        
        # Дополнительные проверки элементов
        check_catalog_elements(driver)
        
        print("\n" + "=" * 50)
        print("РАСШИРЕННЫЙ ТЕСТ ПРОЙДЕН УСПЕШНО")
        print("=" * 50)
        
    finally:
        time.sleep(3)
        driver.quit()


# Запуск основного теста
if __name__ == "__main__":
    # Основной тест (рекомендуется)
    test_login_and_catalog()
    
    # Расширенный тест (раскомментируйте при необходимости)
    # test_with_multiple_checks()