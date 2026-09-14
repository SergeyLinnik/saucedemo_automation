"""
Негативный тест авторизации на сайте Saucedemo.com
Проверка отображения ошибки и закрытия сообщения об ошибке
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
        headless: Если True, браузер запускается в headless режиме
    
    Returns:
        webdriver.Firefox: Настроенный экземпляр драйвера
    """
    firefox_options = FirefoxOptions()
    
    if headless:
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--window-size=1920,1080")
        print("Запуск в HEADLESS режиме")
    else:
        firefox_options.add_argument("--start-maximized")
        print("Запуск в ОБЫЧНОМ режиме")
    
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


def get_error_message(driver: webdriver.Firefox) -> str:
    """
    Получение текста сообщения об ошибке авторизации
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Returns:
        str: Текст сообщения об ошибке
    
    Raises:
        NoSuchElementException: Если элемент с ошибкой не найден
    """
    # Поиск контейнера с ошибкой
    error_container = driver.find_element(By.XPATH, "//div[@class='error-message-container error']")
    
    # Поиск текста ошибки внутри контейнера
    error_text_element = error_container.find_element(By.XPATH, ".//h3")
    error_text = error_text_element.text
    
    return error_text


def is_error_displayed(driver: webdriver.Firefox) -> bool:
    """
    Проверка отображения сообщения об ошибке
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Returns:
        bool: True если ошибка отображается, иначе False
    """
    try:
        error_container = driver.find_element(By.XPATH, "//div[@class='error-message-container error']")
        return error_container.is_displayed()
    except NoSuchElementException:
        return False


def click_error_close_button(driver: webdriver.Firefox) -> None:
    """
    Нажатие на кнопку закрытия сообщения об ошибке
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Raises:
        NoSuchElementException: Если кнопка закрытия не найдена
    """
    # Кнопка закрытия ошибки - это кнопка с крестиком
    close_button = driver.find_element(By.XPATH, "//button[@class='error-button']")
    close_button.click()
    print("Кнопка закрытия ошибки нажата")


def is_error_closed(driver: webdriver.Firefox) -> bool:
    """
    Проверка, что сообщение об ошибке закрыто
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Returns:
        bool: True если ошибка не отображается, иначе False
    """
    time.sleep(0.5)  # Небольшая задержка для анимации закрытия
    return not is_error_displayed(driver)


def wait_for_error_message(driver: webdriver.Firefox, timeout: int = 5) -> None:
    """
    Ожидание появления сообщения об ошибке
    
    Args:
        driver: Экземпляр веб-драйвера
        timeout: Максимальное время ожидания в секундах
    
    Raises:
        TimeoutException: Если сообщение об ошибке не появилось
    """
    wait = WebDriverWait(driver, timeout)
    wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='error-message-container error']")))


def verify_url_not_changed(driver: webdriver.Firefox) -> None:
    """
    Проверка, что URL не изменился (авторизация не выполнена)
    
    Args:
        driver: Экземпляр веб-драйвера
    
    Raises:
        AssertionError: Если URL изменился (авторизация выполнена)
    """
    current_url = driver.current_url
    assert "inventory.html" not in current_url, \
        f"ОШИБКА: Авторизация не должна была пройти, но URL изменился на {current_url}"
    
    assert "saucedemo.com" in current_url, \
        f"ОШИБКА: Текущий URL не соответствует странице логина: {current_url}"


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
    """
    if len(sys.argv) > 1:
        headless_args = ["--headless", "-h", "--no-gui", "-ng"]
        for arg in headless_args:
            if arg in sys.argv:
                return True
    return False


def test_negative_login_invalid_password() -> None:
    """
    НЕГАТИВНЫЙ ТЕСТ 1: Неверный пароль
    """
    """
    ==================================================
    НЕГАТИВНЫЙ ТЕСТ 1: НЕВЕРНЫЙ ПАРОЛЬ
    ==================================================
    """
    
    driver = None
    
    try:
        print("\n[ТЕСТ 1] Авторизация с неверным паролем")
        
        # Создание драйвера
        driver = get_driver(headless=parse_headless_argument())
        
        # Открытие страницы логина
        open_login_page(driver)
        
        # Ввод правильного логина и НЕВЕРНОГО пароля
        enter_username(driver, "standard_user")
        enter_password(driver, "wrong_password")
        
        # Нажатие кнопки входа
        click_login_button(driver)
        
        # Ожидание появления сообщения об ошибке
        wait_for_error_message(driver)
        
        # ПРОВЕРКА 1: Сообщение об ошибке отображается
        assert is_error_displayed(driver), "ОШИБКА: Сообщение об ошибке не отображается"
        print("✅ Проверка 1 пройдена: Сообщение об ошибке отображается")
        
        # ПРОВЕРКА 2: Текст ошибки соответствует ожидаемому
        error_text = get_error_message(driver)
        expected_text = "Epic sadface: Username and password do not match any user in this service"
        assert error_text == expected_text, \
            f"ОШИБКА: Текст ошибки не соответствует. Ожидалось: '{expected_text}', Получено: '{error_text}'"
        print(f"✅ Проверка 2 пройдена: Текст ошибки корректен")
        
        # ПРОВЕРКА 3: URL не изменился (авторизация не выполнена)
        verify_url_not_changed(driver)
        print("✅ Проверка 3 пройдена: URL не изменился")
        
        # ДЕЙСТВИЕ: Клик на кнопку закрытия ошибки
        click_error_close_button(driver)
        
        # ПРОВЕРКА 4: Ошибка закрылась
        assert is_error_closed(driver), "ОШИБКА: Сообщение об ошибке не закрылось"
        print("✅ Проверка 4 пройдена: Сообщение об ошибке успешно закрыто")
        
        print("\n✅✅✅ НЕГАТИВНЫЙ ТЕСТ 1 (НЕВЕРНЫЙ ПАРОЛЬ) ПРОЙДЕН")
        
    except Exception as error:
        print(f"\n❌ ОШИБКА В ТЕСТЕ 1: {error}")
        raise
    
    finally:
        if driver:
            close_driver(driver)


def test_negative_login_invalid_username() -> None:
    """
    НЕГАТИВНЫЙ ТЕСТ 2: Неверный логин
    """
    """
    ==================================================
    НЕГАТИВНЫЙ ТЕСТ 2: НЕВЕРНЫЙ ЛОГИН
    ==================================================
    """
    
    driver = None
    
    try:
        print("\n[ТЕСТ 2] Авторизация с неверным логином")
        
        # Создание драйвера
        driver = get_driver(headless=parse_headless_argument())
        
        # Открытие страницы логина
        open_login_page(driver)
        
        # Ввод НЕВЕРНОГО логина и правильного пароля
        enter_username(driver, "wrong_user")
        enter_password(driver, "secret_sauce")
        
        # Нажатие кнопки входа
        click_login_button(driver)
        
        # Ожидание появления сообщения об ошибке
        wait_for_error_message(driver)
        
        # ПРОВЕРКА: Сообщение об ошибке отображается
        assert is_error_displayed(driver), "ОШИБКА: Сообщение об ошибке не отображается"
        print("✅ Проверка пройдена: Сообщение об ошибке отображается")
        
        # Проверка текста ошибки
        error_text = get_error_message(driver)
        expected_text = "Epic sadface: Username and password do not match any user in this service"
        assert error_text == expected_text, f"Текст ошибки: {error_text}"
        print("✅ Проверка пройдена: Текст ошибки корректен")
        
        # Проверка URL
        verify_url_not_changed(driver)
        print("✅ Проверка пройдена: URL не изменился")
        
        # Закрытие ошибки
        click_error_close_button(driver)
        assert is_error_closed(driver), "Ошибка не закрылась"
        print("✅ Проверка пройдена: Сообщение об ошибке закрыто")
        
        print("\n✅✅✅ НЕГАТИВНЫЙ ТЕСТ 2 (НЕВЕРНЫЙ ЛОГИН) ПРОЙДЕН")
        
    except Exception as error:
        print(f"\n❌ ОШИБКА В ТЕСТЕ 2: {error}")
        raise
    
    finally:
        if driver:
            close_driver(driver)


def test_negative_login_empty_fields() -> None:
    """
    НЕГАТИВНЫЙ ТЕСТ 3: Пустые поля логина и пароля
    """
    """
    ==================================================
    НЕГАТИВНЫЙ ТЕСТ 3: ПУСТЫЕ ПОЛЯ
    ==================================================
    """
    
    driver = None
    
    try:
        print("\n[ТЕСТ 3] Авторизация с пустыми полями")
        
        # Создание драйвера
        driver = get_driver(headless=parse_headless_argument())
        
        # Открытие страницы логина
        open_login_page(driver)
        
        # Оставляем поля пустыми (не вводим логин и пароль)
        # Просто нажимаем кнопку входа
        click_login_button(driver)
        
        # Ожидание появления сообщения об ошибке
        wait_for_error_message(driver)
        
        # ПРОВЕРКА: Сообщение об ошибке отображается
        assert is_error_displayed(driver), "ОШИБКА: Сообщение об ошибке не отображается"
        print("✅ Проверка пройдена: Сообщение об ошибке отображается")
        
        # Проверка текста ошибки (для пустых полей свой текст)
        error_text = get_error_message(driver)
        expected_text = "Epic sadface: Username is required"
        assert error_text == expected_text, \
            f"Ожидался текст: '{expected_text}', Получен: '{error_text}'"
        print("✅ Проверка пройдена: Текст ошибки корректен")
        
        # Проверка URL
        verify_url_not_changed(driver)
        print("✅ Проверка пройдена: URL не изменился")
        
        # Закрытие ошибки
        click_error_close_button(driver)
        assert is_error_closed(driver), "Ошибка не закрылась"
        print("✅ Проверка пройдена: Сообщение об ошибке закрыто")
        
        print("\n✅✅✅ НЕГАТИВНЫЙ ТЕСТ 3 (ПУСТЫЕ ПОЛЯ) ПРОЙДЕН")
        
    except Exception as error:
        print(f"\n❌ ОШИБКА В ТЕСТЕ 3: {error}")
        raise
    
    finally:
        if driver:
            close_driver(driver)


def test_negative_login_locked_user() -> None:
    """
    НЕГАТИВНЫЙ ТЕСТ 4: Заблокированный пользователь
    """
    """
    ==================================================
    НЕГАТИВНЫЙ ТЕСТ 4: ЗАБЛОКИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ
    ==================================================
    """
    
    driver = None
    
    try:
        print("\n[ТЕСТ 4] Авторизация заблокированного пользователя")
        
        # Создание драйвера
        driver = get_driver(headless=parse_headless_argument())
        
        # Открытие страницы логина
        open_login_page(driver)
        
        # Ввод данных заблокированного пользователя
        enter_username(driver, "locked_out_user")
        enter_password(driver, "secret_sauce")
        
        # Нажатие кнопки входа
        click_login_button(driver)
        
        # Ожидание появления сообщения об ошибке
        wait_for_error_message(driver)
        
        # ПРОВЕРКА: Сообщение об ошибке отображается
        assert is_error_displayed(driver), "ОШИБКА: Сообщение об ошибке не отображается"
        print("✅ Проверка пройдена: Сообщение об ошибке отображается")
        
        # Проверка текста ошибки для заблокированного пользователя
        error_text = get_error_message(driver)
        expected_text = "Epic sadface: Sorry, this user has been locked out."
        assert error_text == expected_text, \
            f"Ожидался текст: '{expected_text}', Получен: '{error_text}'"
        print("✅ Проверка пройдена: Текст ошибки корректен")
        
        # Проверка URL
        verify_url_not_changed(driver)
        print("✅ Проверка пройдена: URL не изменился")
        
        # Закрытие ошибки
        click_error_close_button(driver)
        assert is_error_closed(driver), "Ошибка не закрылась"
        print("✅ Проверка пройдена: Сообщение об ошибке закрыто")
        
        print("\n✅✅✅ НЕГАТИВНЫЙ ТЕСТ 4 (ЗАБЛОКИРОВАННЫЙ ПОЛЬЗОВАТЕЛЬ) ПРОЙДЕН")
        
    except Exception as error:
        print(f"\n❌ ОШИБКА В ТЕСТЕ 4: {error}")
        raise
    
    finally:
        if driver:
            close_driver(driver)


def run_all_negative_tests() -> None:
    """
    Запуск всех негативных тестов
    """
    """
    ==================================================
    ЗАПУСК ВСЕХ НЕГАТИВНЫХ ТЕСТОВ
    ==================================================
    """
    
    print("\n" + "=" * 60)
    print("ЗАПУСК НЕГАТИВНЫХ ТЕСТОВ АВТОРИЗАЦИИ")
    print("=" * 60)
    
    # Тест 1: Неверный пароль
    test_negative_login_invalid_password()
    
    # Тест 2: Неверный логин
    test_negative_login_invalid_username()
    
    # Тест 3: Пустые поля
    test_negative_login_empty_fields()
    
    # Тест 4: Заблокированный пользователь
    test_negative_login_locked_user()
    
    print("\n" + "=" * 60)
    print("ВСЕ НЕГАТИВНЫЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ")
    print("=" * 60)


# Точка входа
if __name__ == "__main__":
    # Запуск всех негативных тестов
    run_all_negative_tests()