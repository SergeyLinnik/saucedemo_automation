"""
Проверки по ТЗ:
2.1 — лимит 100 единиц товара
2.2 — лимит 100 000 ₽
2.1 — картинка, описание, вес у каждого товара
3.2 — сообщение в пустой корзине
4.1 — alt у картинок
4.2 — данные корзины на /checkout
"""
import time

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from config import MAX_CART_TOTAL, MAX_UNITS_PER_PRODUCT
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


# ---------- Хелперы ----------

TEST_PRODUCTS = {"Negative Price", "Cart Test Item", "Updated Product", "Автотест товар"}


def _clear_cart(driver) -> None:
    """Полностью очищает корзину через уменьшение количества до 0."""
    driver.get("http://91.197.96.80/cart")
    time.sleep(2)

    cart = CartPage(driver)
    for _ in range(20):  # максимум 20 итераций, чтобы избежать бесконечного цикла
        items = cart.get_cart_items()
        if not items:
            break
        first = items[0]
        qty = cart.get_item_quantity(first)
        for _ in range(qty):
            cart.decrease_quantity(first)
        time.sleep(0.5)


def _skip_test_product(name: str) -> bool:
    """Пропускаем товары, созданные автотестами админки."""
    return name in TEST_PRODUCTS


# ---------- Лимиты из ТЗ ----------

def test_max_units_per_product(driver_buyer):
    """ТЗ 2.1: не более 100 единиц одного товара."""
    _clear_cart(driver_buyer)

    driver_buyer.get("http://91.197.96.80/")
    time.sleep(2)

    inventory = InventoryPage(driver_buyer)
    card = inventory.get_first_card()

    for _ in range(105):
        inventory.increase_quantity(card)

    quantity = inventory.get_product_quantity(card)
    assert quantity <= MAX_UNITS_PER_PRODUCT, (
        f"БАГ (ТЗ 2.1): в корзину добавлено {quantity} единиц, лимит — {MAX_UNITS_PER_PRODUCT}"
    )


def test_max_cart_total(driver_buyer):
    """ТЗ 2.2: сумма заказа не более 100 000 ₽."""
    _clear_cart(driver_buyer)

    driver_buyer.get("http://91.197.96.80/")
    time.sleep(2)

    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()

    max_price = 0.0
    expensive_card = cards[0]
    for card in cards:
        try:
            price = inventory.get_product_price(card)
        except (ValueError, TypeError):
            continue
        if price > max_price:
            max_price = price
            expensive_card = card

    if max_price <= 0:
        pytest.skip("Не удалось определить цену товара")

    needed = min(int(MAX_CART_TOTAL / max_price) + 5, 200)
    for _ in range(needed):
        inventory.increase_quantity(expensive_card)
        if inventory.get_cart_counter() >= MAX_CART_TOTAL / max_price:
            break

    inventory.open_cart()
    cart = CartPage(driver_buyer)
    total = cart.get_total_price()
    assert total <= MAX_CART_TOTAL, (
        f"БАГ (ТЗ 2.2): сумма заказа {total} ₽ превышает лимит {MAX_CART_TOTAL} ₽"
    )


# ---------- Каталог (ТЗ 2.1) ----------

def test_all_products_have_images(driver_buyer):
    """ТЗ 2.1: у каждого товара есть изображение."""
    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()
    assert len(cards) > 0, "Нет товаров"

    missing = []
    for card in cards:
        name = inventory.get_product_name(card)
        if _skip_test_product(name):
            continue
        try:
            img = card.find_element(By.CSS_SELECTOR, ".store-card-image img")
            src = img.get_attribute("src")
            if not src or not src.strip():
                missing.append(name)
        except NoSuchElementException:
            missing.append(name)

    assert not missing, f"БАГ (ТЗ 2.1): нет изображений у товаров: {missing}"


def test_all_products_have_description(driver_buyer):
    """ТЗ 2.1: у каждого товара есть описание (не заглушка 'string')."""
    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()
    bad = []

    for card in cards:
        try:
            body = card.find_element(By.CSS_SELECTOR, ".card-body")
            lines = [ln.strip() for ln in body.text.split("\n") if ln.strip()]
            if not lines:
                continue
            name = lines[0]
            if _skip_test_product(name):
                continue
            if len(lines) < 2:
                bad.append(f"{name}: описание отсутствует")
            elif lines[1].lower() in ("string", ""):
                bad.append(f"{name}: описание = '{lines[1]}'")
        except NoSuchElementException:
            continue

    assert not bad, f"БАГ (ТЗ 2.1): некорректное описание у {len(bad)} товаров. Примеры: {bad[:3]}"


def test_all_products_have_weight(driver_buyer):
    """ТЗ 2.1: у каждого товара указан вес/объём."""
    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()
    no_weight = []

    for card in cards:
        name = inventory.get_product_name(card)
        if _skip_test_product(name):
            continue
        try:
            body = card.find_element(By.CSS_SELECTOR, ".card-body")
            text = body.text.lower()
            markers = [" г", "г ", "гр", "мл", " кг", " л ", "кг"]
            if not any(m in text for m in markers):
                no_weight.append(name)
        except NoSuchElementException:
            continue

    assert not no_weight, (
        f"БАГ (ТЗ 2.1): нет веса у {len(no_weight)} товаров. Примеры: {no_weight[:3]}"
    )


def test_images_have_meaningful_alt(driver_buyer):
    """ТЗ 4.1: alt у изображений должен быть информативным."""
    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()
    bad_alt = []

    for card in cards:
        try:
            img = card.find_element(By.CSS_SELECTOR, ".store-card-image img")
            alt = (img.get_attribute("alt") or "").strip()
            if alt in ("", "...", "image", "img"):
                name = inventory.get_product_name(card)
                if _skip_test_product(name):
                    continue
                bad_alt.append(f"{name} (alt='{alt}')")
        except NoSuchElementException:
            continue

    assert not bad_alt, (
        f"БАГ (ТЗ 4.1): неинформативный alt у {len(bad_alt)} товаров. Примеры: {bad_alt[:3]}"
    )


# ---------- Корзина и оформление ----------

def test_empty_cart_shows_message(driver_buyer):
    """ТЗ 3.2: пустая корзина → сообщение «В корзине пока пусто»."""
    _clear_cart(driver_buyer)

    driver_buyer.refresh()
    time.sleep(2)
    page_text = driver_buyer.find_element(By.TAG_NAME, "body").text.lower()

    assert "пусто" in page_text, (
        "БАГ (ТЗ 3.2): нет сообщения «В корзине пока пусто». "
        f"Текст страницы: {page_text[:200]}"
    )


def test_checkout_shows_cart_data(driver_buyer):
    """ТЗ 4.2: на /checkout должны передаваться данные корзины."""
    _clear_cart(driver_buyer)

    driver_buyer.get("http://91.197.96.80/")
    time.sleep(2)

    inventory = InventoryPage(driver_buyer)
    inventory.increase_quantity(inventory.get_first_card())
    inventory.open_cart()

    cart = CartPage(driver_buyer)
    cart.checkout()
    time.sleep(2)

    page_text = driver_buyer.find_element(By.TAG_NAME, "body").text.lower()
    # На /checkout должно быть упоминание суммы или товаров
    has_data = ("₽" in page_text) or ("итого" in page_text) or ("сумма" in page_text)
    assert has_data, (
        "БАГ (ТЗ 4.2): на странице /checkout нет данных корзины (ни суммы, ни товаров)"
    )