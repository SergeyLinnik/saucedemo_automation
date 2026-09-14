from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator, text):
        """
        Кастомный метод для ввода текста.
        Решает проблему с кириллицей через JavaScript и уведомляет Vue.js об изменении.
        """
        element = self.find_element(locator)
        # Очищаем поле
        self.driver.execute_script("arguments[0].value = '';", element)
        # Вводим текст через JS
        self.driver.execute_script(f"arguments[0].value = '{text}';", element)
        # ВАЖНО: Говорим Vue.js, что значение изменилось (триггерим событие input)
        self.driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", element)