"""Все локаторы элементов в одном месте."""
from selenium.webdriver.common.by import By
from typing import Tuple

Locator = Tuple[str, str]


class LoginLocators:
    USERNAME_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Логин']")
    PASSWORD_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Пароль']")
    LOGIN_BUTTON: Locator = (By.XPATH, "//button[contains(text(), 'Войти')]")


class InventoryLocators:
    PRODUCT_CARDS: Locator = (By.CSS_SELECTOR, ".store-card")
    CART_LINK: Locator = (By.CSS_SELECTOR, "a[href='/cart']")
    CART_COUNTER: Locator = (By.CSS_SELECTOR, ".cart-counter")
    CARD_BODY: Locator = (By.CSS_SELECTOR, ".card-body")
    QUANTITY_INPUT: Locator = (By.XPATH, ".//input[@type='text']")
    ADD_BUTTON: Locator = (By.XPATH, ".//button[.//span[text()='add']]")
    REMOVE_BUTTON: Locator = (By.XPATH, ".//button[.//span[text()='remove']]")
    PRICE: Locator = (By.XPATH, ".//div[contains(@class,'fs-5')]")


class CartLocators:
    CART_ITEMS: Locator = (By.CSS_SELECTOR, ".store-card")
    TOTAL_TEXT: Locator = (By.XPATH, "//div[contains(text(),'Итого')]")
    CHECKOUT_BUTTON: Locator = (By.XPATH, "//button[contains(text(),'Оформить заказ')]")
    CARD_BODY: Locator = InventoryLocators.CARD_BODY
    QUANTITY_INPUT: Locator = InventoryLocators.QUANTITY_INPUT
    ADD_BUTTON: Locator = InventoryLocators.ADD_BUTTON
    REMOVE_BUTTON: Locator = InventoryLocators.REMOVE_BUTTON
    PRICE: Locator = InventoryLocators.PRICE


class AdminLocators:
    PRODUCT_CARDS: Locator = (By.CSS_SELECTOR, ".store-card")
    EDIT_BUTTON: Locator = (By.XPATH, ".//button[contains(., 'edit')]")
    DELETE_BUTTON: Locator = (By.XPATH, ".//button[contains(., 'delete')]")
    ADD_PRODUCT_BUTTON: Locator = (By.XPATH, "//button[contains(text(),'Добавить товар')]")

    NAME_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Наименование']")
    DESCRIPTION_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Описание']")
    EXPECTED_CATEGORY_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder*='жидаемая']")
    CATEGORY_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Категория в списке']")
    PRICE_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Цена']")
    IMAGE_INPUT: Locator = (By.CSS_SELECTOR, "input[placeholder='Image Source']")

    CREATE_BUTTON: Locator = (By.XPATH, "//button[contains(text(),'Создать товар')]")
    INVALID_FIELD: Locator = (By.CSS_SELECTOR, ".is-invalid")
    SELECT_ELEMENT: Locator = (By.CSS_SELECTOR, "select")