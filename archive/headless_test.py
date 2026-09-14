"""
Тест авторизации на сайте Saucedemo.com с поддержкой headless режима
Headless режим - запуск браузера без графического интерфейса
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys


def get_driver(headless: bool = False) -> webdriver.Firefox:
    """
    Создание и настройка драйвера браузера Firefox
    
    Args:
        headless: Если True, браузер запускается в headless режиме (без GUI)
    
    Returns:
        webdriver.Firefox: Настроенный экземпляр драйвера
    
    Примеры:
        driver = get_driver()              # Обычный режим
        driver = get_driver(headless=True) # Headless режим
    """
    # Настройка опций Firefox
    firefox_options = FirefoxOptions()
    
    if headless:
        # Headless режим: браузер работает в фоне, окно не отображается
        firefox_options.add_argument("--headless")
        # Для headless режима нужно указать размер окна
        firefox_options.add_argument("--window-size=1920,1080")
        print("Запуск в HEADLESS режиме (без графического интерфейса)")
    else:
        # Обычный режим: браузер отображается на экране
        firefox_options.add_argument("--start-maximized")
        print("Запуск в ОБЫЧНОМ режиме (с графическим интерфейсом)")
    
    # Создание и настройка драйвера
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=firefox_options)
    
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


def close_driver(driver: webdriver.Firefox) -> None:
    """
    Закрытие драйвера и браузера
    
    Args:
        driver: Экземпляр веб-драйвера
    """
    time.sleep(1)
    driver.quit()


def parse_headless_argument() -> bool:
    """
    Разбор аргументов командной строки для определения headless режима
    
    Returns:
        bool: True если запуск в headless режиме, иначе False
    
    Примеры запуска:
        python headless_test.py          # Обычный режим
        python headless_test.py --headless  # Headless режим
        python headless_test.py -h       # Headless режим (краткая форма)
    """
    # Проверка аргументов командной строки
    if len(sys.argv) > 1:
        headless_args = ["--headless", "-h", "--no-gui", "-ng"]
        for arg in headless_args:
            if arg in sys.argv:
                return True
    return False


def print_usage() -> None:
    """
    Вывод справки по использованию скрипта
    """
    print("""
    ================================================
    ИСПОЛЬЗОВАНИЕ СКРИПТА
    ================================================
    
    Запуск в обычном режиме (с отображением окна браузера):
        python headless_test.py
    
    Запуск в headless режиме (без отображения окна браузера):
        python headless_test.py --headless
        python headless_test.py -h
        python headless_test.py --no-gui
        python headless_test.py -ng
    
    Headless режим полезен для:
    - CI/CD пайплайнов (Jenkins, GitLab CI, GitHub Actions)
    - Запуска тестов на серверах без графического интерфейса
    - Ускорения выполнения тестов
    - Параллельного запуска нескольких тестов
    """)


def test_login_and_catalog(headless: bool = False) -> None:
    """
    Основная функция теста авторизации и проверки каталога
    
    Args:
        headless: Запускать ли браузер в headless режиме
    """
    """
    ==================================================
    ТЕСТ АВТОРИЗАЦИИ И ПРОВЕРКИ СТРАНИЦЫ КАТАЛОГА
    ==================================================
    """
    
    driver = None
    
    # Вывод информации о режиме запуска
    if headless:
        print("\n[INFO] Запуск в HEADLESS режиме (окно браузера не отображается)")
    else:
        print("\n[INFO] Запуск в ОБЫЧНОМ режиме (окно браузера отображается)")
    
    try:
        # Шаг 1: Создание драйвера с учетом headless режима
        driver = get_driver(headless=headless)
        
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
        
        # Вывод результата
        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ ТЕСТА:")
        print("=" * 50)
        print("✅ URL соответствует ожидаемому")
        print("✅ Страница каталога успешно загружена")
        print("✅ Товары отображаются в каталоге")
        
        mode_text = "HEADLESS" if headless else "ОБЫЧНЫЙ"
        print(f"✅ Режим запуска: {mode_text}")
        
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


# Точка входа
if __name__ == "__main__":
    # Проверка аргументов для вывода справки
    if "--help" in sys.argv or "-?" in sys.argv:
        print_usage()
        sys.exit(0)
    
    # Определение режима запуска
    headless_mode = parse_headless_argument()
    
    # Запуск теста
    test_login_and_catalog(headless=headless_mode)