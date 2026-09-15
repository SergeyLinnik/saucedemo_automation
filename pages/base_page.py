"""Базовый класс для всех страниц."""
from typing import Tuple

from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import DEFAULT_TIMEOUT
from pages.exceptions import ElementNotFoundError

Locator = Tuple[str, str]


class BasePage:
    """Общие методы взаимодействия с элементами."""

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def find_element(self, locator: Locator) -> WebElement:
        """Ждёт появления элемента, иначе — ElementNotFoundError."""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException as exc:
            raise ElementNotFoundError(
                f"Элемент {locator} не найден за {DEFAULT_TIMEOUT} секунд"
            ) from exc

    def click(self, locator: Locator) -> None:
        """Ждёт кликабельности и кликает."""
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except TimeoutException as exc:
            raise ElementNotFoundError(
                f"Кликабельный элемент {locator} не появился"
            ) from exc

    def enter_text(self, locator: Locator, text: str) -> None:
        """
        Вводит текст через JS. Обходит проблему с кириллицей
        в Selenium и уведомляет Vue.js об изменении поля.
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].value = '';", element)
        self.driver.execute_script(f"arguments[0].value = '{text}';", element)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            element,
        )

    def get_text(self, locator: Locator) -> str:
        return self.find_element(locator).text

    @staticmethod
    def element_exists(parent: WebElement, locator: Locator) -> bool:
        """Проверяет наличие дочернего элемента без ожидания."""
        try:
            parent.find_element(*locator)
            return True
        except NoSuchElementException:
            return False