"""
Тест авторизации на сайте Saucedemo.com
Проверка URL и страницы каталога после входа
С учетом принципов SRP и правильной обработки исключений
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def get_driver() -> webdriver.Firefox:
    """
    Создание и настройка драйвера браузера
    
    Returns:
        webdriver.Firefox: Настроенный экземпляр драйвера
    """
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    driver.maximize_window()
    return driver


def open_login_page(driver: webdriver.Firefox) -> None:
    """
    Открытие страницы логина
    
    Args:
        driver: Экземпляр веб-драйвера
    """
    driver.get("https://www.saucedemo.com/")


def enter_username(driver: webdriver.Firefox, username: str) -> None:
    """
    Ввод логина в поле авторизации
    
    Args:
        driver: Экземпляр веб-драйвера
        username: Логин для ввода
    """
    username_field = driver.find_element(By.XPATH, "//input[@id='user-name']")
    username_field.clear()
    username_field.send_keys(username)


def enter_password(driver: webdriver.Firefox, password: str) -> None:
    """
    Ввод пароля в поле авторизации
    
    Args:
        driver: Экземпляр веб-драйвера
        password: Пароль для ввода
    """
    password_field = driver.find_element(By.XPATH, "//input[@id='password']")
    password_field.clear()
    password_field.send_keys(password)


def click_login_button(driver: webdriver.Firefox) -> None:
    """
    Нажатие кнопки авторизации
    
    Args:
        driver: Экземпляр веб-драйвера
    """
    login_button = driver.find_element(By.XPATH, "//input[@id='login-button']")
    login_button.click()


def wait_for_inventory_page(driver: webdriver.Firefox, timeout: int = 10) -> None:
    """
    Ожидание загрузки страницы инвентаря после авторизации
    
    Args:
        driver: Экземпляр веб-драйвера
        timeout: Максимальное время ожидания в секундах
    
    Raises:
        TimeoutException: Если страница не загрузилась за отведенное время
    """
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.url_contains("inventory.html"))


def verify_url_contains(driver: webdriver.Firefox, expected_part: str) -> None:
    """
    Проверка, что URL содержит ожидаемую часть
    
    Args:
        driver: Экземпляр веб-драйвера
        expected_part: Ожидаемая часть URL
    
    Raises:
        AssertionError: Если URL не содержит ожидаемую часть
    """
    current_url = driver.current_url
    assert expected_part in current_url, \
        f"URL не содержит '{expected_part}'. Текущий URL: {current_url}"


def verify_catalog_page(driver: webdriver.Firefox) -> None:
    """
    Проверка, что открыта страница каталога
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Raises:
        AssertionError: Если страница каталога не загружена
    """
    # Проверка заголовка страницы
    page_title = driver.title
    assert page_title == "Swag Labs", \
        f"Заголовок страницы '{page_title}' не соответствует 'Swag Labs'"
    
    # Проверка наличия контейнера каталога
    inventory_container = driver.find_element(By.XPATH, "//div[@class='inventory_container']")
    assert inventory_container.is_displayed(), "Контейнер каталога не отображается"


def verify_inventory_items(driver: webdriver.Firefox) -> None:
    """
    Проверка наличия товаров в каталоге
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Raises:
        AssertionError: Если товары не найдены
    """
    inventory_items = driver.find_elements(By.XPATH, "//div[@class='inventory_item']")
    assert len(inventory_items) > 0, "В каталоге не найдено товаров"


def verify_catalog_controls(driver: webdriver.Firefox) -> None:
    """
    Проверка наличия элементов управления на странице каталога
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Raises:
        AssertionError: Если элементы управления отсутствуют
    """
    # Проверка фильтрации товаров
    filter_dropdown = driver.find_element(By.XPATH, "//select[@class='product_sort_container']")
    assert filter_dropdown.is_displayed(), "Элемент фильтрации не отображается"
    
    # Проверка корзины
    shopping_cart = driver.find_element(By.XPATH, "//div[@id='shopping_cart_container']")
    assert shopping_cart.is_displayed(), "Корзина не отображается"


def close_driver(driver: webdriver.Firefox) -> None:
    """
    Закрытие драйвера и браузера
    
    Args:
        driver: Экземпляр веб-драйвера
    """
    time.sleep(2)
    driver.quit()


def test_login_and_catalog() -> None:
    """
    Основная функция теста авторизации и проверки каталога
    Вызывает все необходимые шаги в правильном порядке
    """
    """
    ==================================================
    ТЕСТ АВТОРИЗАЦИИ И ПРОВЕРКИ СТРАНИЦЫ КАТАЛОГА
    ==================================================
    """
    
    driver = None
    
    try:
        # Шаг 1: Создание драйвера
        driver = get_driver()
        
        # Шаг 2: Открытие страницы логина
        open_login_page(driver)
        
        # Шаг 3: Ввод логина
        enter_username(driver, "standard_user")
        
        # Шаг 4: Ввод пароля
        enter_password(driver, "secret_sauce")
        
        # Шаг 5: Нажатие кнопки авторизации
        click_login_button(driver)
        
        # Шаг 6: Ожидание загрузки страницы инвентаря
        wait_for_inventory_page(driver)
        
        # Шаг 7: Проверка URL
        verify_url_contains(driver, "inventory.html")
        
        # Шаг 8: Проверка страницы каталога
        verify_catalog_page(driver)
        
        # Шаг 9: Проверка наличия товаров
        verify_inventory_items(driver)
        
        # Шаг 10: Проверка элементов управления
        verify_catalog_controls(driver)
        
        # Вывод результата
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 50)
        print("✅ URL соответствует ожидаемому")
        print("✅ Страница каталога успешно загружена")
        print("✅ Товары отображаются в каталоге")
        print("✅ Элементы управления (фильтр, корзина) присутствуют")
        
    except TimeoutException as error:
        print(f"\n❌ ОШИБКА ВРЕМЕНИ ОЖИДАНИЯ: Страница не загрузилась за отведенное время")
        print(f"   Детали: {error}")
        raise
    
    except NoSuchElementException as error:
        print(f"\n❌ ОШИБКА: Элемент не найден на странице")
        print(f"   Детали: {error}")
        raise
    
    except AssertionError as error:
        print(f"\n❌ ОШИБКА ПРОВЕРКИ: {error}")
        raise
    
    finally:
        # Закрытие драйвера
        if driver:
            close_driver(driver)
            print("\nТест авторизации и проверки каталога завершен")


# Запуск теста
if __name__ == "__main__":
    test_login_and_catalog()