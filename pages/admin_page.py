"""Страницы администратора: список товаров, редактирование, создание."""
import time
from typing import List, Optional

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from config import (
    ADMIN_CREATE_URL,
    ADMIN_MANAGE_URL,
    ANIMATION_DELAY,
)
from pages.base_page import BasePage
from pages.exceptions import (
    ButtonDisabledError,
    EmptyProductListError,
    FormValidationError,
)
from pages.locators import AdminLocators


class AdminPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    # ---------- Навигация ----------

    def open_manage_page(self) -> None:
        self.driver.get(ADMIN_MANAGE_URL)
        time.sleep(ANIMATION_DELAY)

    def open_create_page(self) -> None:
        self.driver.get(ADMIN_CREATE_URL)
        time.sleep(ANIMATION_DELAY)

    # ---------- Список товаров ----------

    def get_product_cards(self) -> List[WebElement]:
        return self.driver.find_elements(*AdminLocators.PRODUCT_CARDS)

    def get_first_card(self) -> WebElement:
        cards = self.get_product_cards()
        if not cards:
            raise EmptyProductListError("Список товаров в админке пуст")
        return cards[0]

    def click_edit_first_product(self) -> str:
        """Нажимает edit у первого товара. Возвращает URL."""
        card = self.get_first_card()
        edit_btn = card.find_element(*AdminLocators.EDIT_BUTTON)
        ActionChains(self.driver).move_to_element(edit_btn).click().perform()
        time.sleep(ANIMATION_DELAY)
        return self.driver.current_url

    def click_add_product(self) -> str:
        """Нажимает «Добавить товар». Возвращает URL."""
        btn = self.find_element(AdminLocators.ADD_PRODUCT_BUTTON)
        ActionChains(self.driver).move_to_element(btn).click().perform()
        time.sleep(ANIMATION_DELAY)
        return self.driver.current_url

    # ---------- Форма ----------

    def _set_input(self, locator, value: str) -> None:
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].value = '';", element)
        self.driver.execute_script(f"arguments[0].value = '{value}';", element)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            element,
        )

    def _get_input(self, locator) -> str:
        return self.find_element(locator).get_attribute("value")

    def set_name(self, value: str) -> None:
        self._set_input(AdminLocators.NAME_INPUT, value)

    def get_name(self) -> str:
        return self._get_input(AdminLocators.NAME_INPUT)

    def _try_set_category(self, value: str) -> Optional[str]:
        """Категория может быть input ИЛИ select — пробуем оба."""
        try:
            el = self.driver.find_element(*AdminLocators.CATEGORY_INPUT)
            self.driver.execute_script("arguments[0].value = '';", el)
            self.driver.execute_script(f"arguments[0].value = '{value}';", el)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", el
            )
            return "input"
        except NoSuchElementException:
            pass

        try:
            selects = self.driver.find_elements(*AdminLocators.SELECT_ELEMENT)
            if selects:
                Select(selects[-1]).select_by_index(0)
                return "select"
        except NoSuchElementException:
            pass

        return None

    def fill_full_form(
        self,
        name: str,
        desc: str,
        expected_cat: str,
        cat: str,
        price: int,
        image: str,
    ) -> None:
        self._set_input(AdminLocators.NAME_INPUT, name)
        self._set_input(AdminLocators.DESCRIPTION_INPUT, desc)
        self._set_input(AdminLocators.EXPECTED_CATEGORY_INPUT, expected_cat)
        self._try_set_category(cat)
        self._set_input(AdminLocators.PRICE_INPUT, str(price))
        self._set_input(AdminLocators.IMAGE_INPUT, image)
        time.sleep(0.5)

    def is_create_button_enabled(self) -> bool:
        btn = self.find_element(AdminLocators.CREATE_BUTTON)
        return btn.is_enabled()

    def click_create(self) -> None:
        btn = self.find_element(AdminLocators.CREATE_BUTTON)
        if not btn.is_enabled():
            raise ButtonDisabledError(
                "Кнопка «Создать товар» заблокирована — заполните все поля"
            )
        ActionChains(self.driver).move_to_element(btn).click().perform()
        time.sleep(ANIMATION_DELAY)

    def count_invalid_fields(self) -> int:
        return len(self.driver.find_elements(*AdminLocators.INVALID_FIELD))

    def assert_form_invalid(self) -> None:
        """Бросает FormValidationError, если форма считается валидной."""
        if self.count_invalid_fields() == 0:
            raise FormValidationError(
                "Пустая форма не помечает поля как .is-invalid"
            )