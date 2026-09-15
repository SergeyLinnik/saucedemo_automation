"""Общие фикстуры для всех тестов."""
import time
from typing import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config import ADMIN_LOGIN, ADMIN_PASSWORD, BASE_URL, BUYER_LOGIN, BUYER_PASSWORD
from pages.login_page import LoginPage


def _create_driver() -> WebDriver:
    options = webdriver.ChromeOptions()
    return webdriver.Chrome(options=options)


def _clean_storage(driver: WebDriver) -> None:
    driver.get(BASE_URL)
    driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
    driver.delete_all_cookies()
    driver.refresh()
    time.sleep(2)


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    """Чистый браузер без авторизации — для тестов логина."""
    d = _create_driver()
    d.maximize_window()
    d.get(BASE_URL)
    yield d
    d.quit()


@pytest.fixture(scope="function")
def driver_buyer() -> Generator[WebDriver, None, None]:
    """Авторизованный покупатель с чистой корзиной."""
    d = _create_driver()
    d.maximize_window()
    _clean_storage(d)
    LoginPage(d).login(BUYER_LOGIN, BUYER_PASSWORD)
    time.sleep(2)
    yield d
    d.quit()


@pytest.fixture(scope="function")
def driver_admin() -> Generator[WebDriver, None, None]:
    """Авторизованный администратор."""
    d = _create_driver()
    d.maximize_window()
    _clean_storage(d)
    LoginPage(d).login(ADMIN_LOGIN, ADMIN_PASSWORD)
    time.sleep(2)
    yield d
    d.quit()