"""Страница каталога товаров."""
import time
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from config import ANIMATION_DELAY
from pages.base_page import BasePage
from pages.exceptions import EmptyProductListError
from pages.locators import InventoryLocators


class InventoryPage(BasePage):
    """Каталог товаров. Содержит методы для работы с карточками."""

    NAME_CANDIDATES: List[str] = ["h5", "h4", "h3", ".card-title", ".product-name"]

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_product_cards(self) -> List[WebElement]:
        return self.driver.find_elements(*InventoryLocators.PRODUCT_CARDS)

    def get_first_card(self) -> WebElement:
        """Первая карточка или EmptyProductListError."""
        cards = self.get_product_cards()
        if not cards:
            raise EmptyProductListError("На странице каталога нет товаров")
        return cards[0]

    def get_product_name(self, card: WebElement) -> str:
        """Ищет название товара несколькими селекторами."""
        for selector in self.NAME_CANDIDATES:
            try:
                element = card.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if text:
                    return text
            except NoSuchElementException:
                continue
        body = card.find_element(*InventoryLocators.CARD_BODY)
        return body.text.split("\n")[0].strip()

    def get_product_price(self, card: WebElement) -> float:
        price_text = card.find_element(*InventoryLocators.PRICE).text
        return float(price_text.replace("₽", "").replace(" ", "").replace(",", "."))

    def get_product_quantity(self, card: WebElement) -> int:
        field = card.find_element(*InventoryLocators.QUANTITY_INPUT)
        return int(field.get_attribute("value"))

    def increase_quantity(self, card: WebElement) -> None:
        button = card.find_element(*InventoryLocators.ADD_BUTTON)
        ActionChains(self.driver).move_to_element(button).click().perform()
        time.sleep(ANIMATION_DELAY)

    def decrease_quantity(self, card: WebElement) -> None:
        button = card.find_element(*InventoryLocators.REMOVE_BUTTON)
        ActionChains(self.driver).move_to_element(button).click().perform()
        time.sleep(ANIMATION_DELAY)

    def get_cart_counter(self) -> int:
        """Счётчик корзины. 0, если элемента нет."""
        try:
            element = self.driver.find_element(*InventoryLocators.CART_COUNTER)
            text = element.text.strip()
            return int(text) if text else 0
        except NoSuchElementException:
            return 0
        except ValueError:
            return 0

    def open_cart(self) -> None:
        self.click(InventoryLocators.CART_LINK)
        time.sleep(ANIMATION_DELAY)