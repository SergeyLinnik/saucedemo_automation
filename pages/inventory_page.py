from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage
import time


class InventoryPage(BasePage):
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".store-card")
    CART_LINK = (By.CSS_SELECTOR, "a[href='/cart']")
    CART_COUNTER = (By.CSS_SELECTOR, ".cart-counter")

    def get_product_cards(self):
        return self.driver.find_elements(*self.PRODUCT_CARDS)

    def get_product_name(self, card):
        for sel in ["h5", "h4", "h3", ".card-title", ".product-name"]:
            try:
                el = card.find_element(By.CSS_SELECTOR, sel)
                if el.text.strip():
                    return el.text.strip()
            except:
                continue
        body = card.find_element(By.CSS_SELECTOR, ".card-body")
        return body.text.split("\n")[0].strip()

    def get_cart_counter(self):
        """Возвращает счётчик корзины. 0, если элемента нет."""
        try:
            el = self.driver.find_element(*self.CART_COUNTER)
            text = el.text.strip()
            return int(text) if text else 0
        except:
            return 0

    def increase_quantity(self, card):
        """Клик через ActionChains (работает надёжнее, чем JS click)"""
        plus_button = card.find_element(By.XPATH, ".//button[.//span[text()='add']]")
        ActionChains(self.driver).move_to_element(plus_button).click().perform()
        time.sleep(1)

    def decrease_quantity(self, card):
        minus_button = card.find_element(By.XPATH, ".//button[.//span[text()='remove']]")
        ActionChains(self.driver).move_to_element(minus_button).click().perform()
        time.sleep(1)

    def open_cart(self):
        self.click(self.CART_LINK)
        time.sleep(1.5)