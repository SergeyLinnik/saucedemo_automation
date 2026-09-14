from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import time


class AdminPage(BasePage):
    ADMIN_URL = "http://91.197.96.80/manageProductsPage"
    CREATE_URL = "http://91.197.96.80/createProduct"

    PRODUCT_CARDS = (By.CSS_SELECTOR, ".store-card")
    # Более гибкий XPath для кнопок
    EDIT_BUTTON = (By.XPATH, ".//button[contains(., 'edit')]")
    DELETE_BUTTON = (By.XPATH, ".//button[contains(., 'delete')]")
    ADD_PRODUCT_BUTTON = (By.XPATH, "//button[contains(text(),'Добавить товар')]")

    NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Наименование']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "input[placeholder='Описание']")
    EXPECTED_CATEGORY_INPUT = (By.CSS_SELECTOR, "input[placeholder*='жидаемая']")
    PRICE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Цена']")
    IMAGE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Image Source']")

    CREATE_BUTTON = (By.XPATH, "//button[contains(text(),'Создать товар')]")

    def open_manage_page(self):
        self.driver.get(self.ADMIN_URL)
        time.sleep(2)

    def open_create_page(self):
        self.driver.get(self.CREATE_URL)
        time.sleep(2)

    def get_product_cards(self):
        return self.driver.find_elements(*self.PRODUCT_CARDS)

    def get_product_name(self, card):
        body = card.find_element(By.CSS_SELECTOR, ".card-body")
        return body.text.split("\n")[0].strip()

    def click_edit_first_product(self):
        cards = self.get_product_cards()
        assert len(cards) > 0, "Список товаров пуст"
        edit_btn = cards[0].find_element(*self.EDIT_BUTTON)
        ActionChains(self.driver).move_to_element(edit_btn).click().perform()
        time.sleep(2)
        return self.driver.current_url

    def click_add_product(self):
        btn = self.find_element(self.ADD_PRODUCT_BUTTON)
        ActionChains(self.driver).move_to_element(btn).click().perform()
        time.sleep(2)
        return self.driver.current_url

    def _set_input(self, locator, value):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].value = '';", element)
        self.driver.execute_script(f"arguments[0].value = '{value}';", element)
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
            element
        )

    def _get_input(self, locator):
        return self.find_element(locator).get_attribute('value')

    def set_name(self, value):
        self._set_input(self.NAME_INPUT, value)

    def get_name(self):
        return self._get_input(self.NAME_INPUT)

    def _try_set_category(self, value):
        """Категория может быть input ИЛИ select. Пробуем оба."""
        # Вариант 1: input
        try:
            el = self.driver.find_element(
                By.CSS_SELECTOR, "input[placeholder='Категория в списке']"
            )
            self.driver.execute_script("arguments[0].value = '';", el)
            self.driver.execute_script(f"arguments[0].value = '{value}';", el)
            self.driver.execute_script(
                "arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", el
            )
            return "input"
        except Exception:
            pass
        # Вариант 2: select
        try:
            selects = self.driver.find_elements(By.CSS_SELECTOR, "select")
            if selects:
                Select(selects[-1]).select_by_index(0)
                return "select"
        except Exception:
            pass
        return None

    def fill_full_form(self, name, desc, expected_cat, cat, price, image):
        self._set_input(self.NAME_INPUT, name)
        self._set_input(self.DESCRIPTION_INPUT, desc)
        self._set_input(self.EXPECTED_CATEGORY_INPUT, expected_cat)
        self._try_set_category(cat)  # может быть input или select
        self._set_input(self.PRICE_INPUT, str(price))
        self._set_input(self.IMAGE_INPUT, image)
        time.sleep(0.5)

    def is_create_button_enabled(self):
        btn = self.find_element(self.CREATE_BUTTON)
        return btn.is_enabled()

    def click_create(self):
        btn = self.find_element(self.CREATE_BUTTON)
        if not btn.is_enabled():
            raise RuntimeError("Кнопка 'Создать товар' заблокирована.")
        ActionChains(self.driver).move_to_element(btn).click().perform()
        time.sleep(2)

    def count_invalid_fields(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, ".is-invalid"))

    def take_screenshot(self, path):
        self.driver.save_screenshot(path)