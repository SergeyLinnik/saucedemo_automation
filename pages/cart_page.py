from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import time


class CartPage(BasePage):
    CART_ITEMS = (By.CSS_SELECTOR, ".store-card")
    TOTAL_TEXT = (By.XPATH, "//div[contains(text(),'Итого')]")
    CHECKOUT_BUTTON = (By.XPATH, "//button[contains(text(),'Оформить заказ')]")

    def get_cart_items(self):
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_item_name(self, card):
        for sel in ["h5", "h4", "h3", ".card-title", ".product-name"]:
            try:
                el = card.find_element(By.CSS_SELECTOR, sel)
                if el.text.strip():
                    return el.text.strip()
            except:
                continue
        body = card.find_element(By.CSS_SELECTOR, ".card-body")
        return body.text.split("\n")[0].strip()

    def get_item_quantity(self, card):
        input_field = card.find_element(By.XPATH, ".//input[@type='text']")
        return int(input_field.get_attribute('value'))

    def increase_quantity(self, card):
        plus_button = card.find_element(By.XPATH, ".//button[.//span[text()='add']]")
        ActionChains(self.driver).move_to_element(plus_button).click().perform()
        time.sleep(1.5)

    def decrease_quantity(self, card):
        minus_button = card.find_element(By.XPATH, ".//button[.//span[text()='remove']]")
        ActionChains(self.driver).move_to_element(minus_button).click().perform()
        time.sleep(1)

    def get_total_price(self):
        text = self.find_element(self.TOTAL_TEXT).text
        number_str = text.replace('Итого:', '').replace('₽', '').replace(' ', '').replace(',', '.')
        return float(number_str)

    def checkout(self):
        self.click(self.CHECKOUT_BUTTON)

    def is_empty(self):
        return len(self.get_cart_items()) == 0