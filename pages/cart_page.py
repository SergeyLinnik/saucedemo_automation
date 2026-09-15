"""Страница корзины."""
import time
from typing import List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from config import ANIMATION_DELAY
from pages.base_page import BasePage
from pages.locators import CartLocators


class CartPage(BasePage):
    NAME_CANDIDATES: List[str] = ["h5", "h4", "h3", ".card-title", ".product-name"]

    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def get_cart_items(self) -> List[WebElement]:
        return self.driver.find_elements(*CartLocators.CART_ITEMS)

    def get_item_name(self, card: WebElement) -> str:
        for selector in self.NAME_CANDIDATES:
            try:
                element = card.find_element(By.CSS_SELECTOR, selector)
                text = element.text.strip()
                if text:
                    return text
            except NoSuchElementException:
                continue
        body = card.find_element(*CartLocators.CARD_BODY)
        return body.text.split("\n")[0].strip()

    def get_item_quantity(self, card: WebElement) -> int:
        field = card.find_element(*CartLocators.QUANTITY_INPUT)
        return int(field.get_attribute("value"))

    def increase_quantity(self, card: WebElement) -> None:
        button = card.find_element(*CartLocators.ADD_BUTTON)
        ActionChains(self.driver).move_to_element(button).click().perform()
        time.sleep(ANIMATION_DELAY)

    def decrease_quantity(self, card: WebElement) -> None:
        button = card.find_element(*CartLocators.REMOVE_BUTTON)
        ActionChains(self.driver).move_to_element(button).click().perform()
        time.sleep(ANIMATION_DELAY)

    def get_total_price(self) -> float:
        """Сумма заказа из блока «Итого»."""
        text = self.get_text(CartLocators.TOTAL_TEXT)
        number = text.replace("Итого:", "").replace("₽", "").replace(" ", "").replace(",", ".")
        return float(number)

    def checkout(self) -> None:
        self.click(CartLocators.CHECKOUT_BUTTON)