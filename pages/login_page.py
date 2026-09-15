"""Страница авторизации."""
from selenium.webdriver.remote.webdriver import WebDriver

from pages.base_page import BasePage
from pages.locators import LoginLocators


class LoginPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)

    def login(self, username: str, password: str) -> None:
        """Авторизует пользователя."""
        self.enter_text(LoginLocators.USERNAME_INPUT, username)
        self.enter_text(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)