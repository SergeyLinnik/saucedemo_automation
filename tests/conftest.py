import pytest
import time
from selenium import webdriver


def _create_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


@pytest.fixture(scope="function")
def driver():
    """Чистый драйвер без логина (для тестов авторизации)"""
    d = _create_driver()
    d.get("http://91.197.96.80/")
    yield d
    d.quit()


@pytest.fixture(scope="function")
def driver_buyer():
    """Покупатель1 (пустая корзина)"""
    d = _create_driver()
    d.get("http://91.197.96.80/")
    d.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    d.delete_all_cookies()
    d.refresh()
    time.sleep(2)
    from pages.login_page import LoginPage
    LoginPage(d).login("покупатель1", "покупатель1")
    time.sleep(2)
    yield d
    d.quit()


@pytest.fixture(scope="function")
def driver_admin():
    """Администратор"""
    d = _create_driver()
    d.get("http://91.197.96.80/")
    d.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    d.delete_all_cookies()
    d.refresh()
    time.sleep(2)
    from pages.login_page import LoginPage
    LoginPage(d).login("admin", "admin")
    time.sleep(2)
    yield d
    d.quit()