from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class LoginPage(BasePage):
    # Ищем по атрибуту placeholder (текст внутри поля)
    USERNAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Логин']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[placeholder='Пароль']")
    # Ищем кнопку по тексту на ней
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")

    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)