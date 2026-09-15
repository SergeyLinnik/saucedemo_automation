"""Граничные значения из ТЗ:
2.1 — не более 100 единиц одного товара в корзине
2.2 — сумма заказа не более 100 000 ₽

Эти тесты ПАДАЮТ, потому что сайт нарушает ТЗ.
"""
import time

import pytest

from config import MAX_CART_TOTAL, MAX_UNITS_PER_PRODUCT
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


def test_max_units_per_product(driver_buyer):
    """
    ТЗ 2.1: не более 100 единиц одного товара.
    БАГ: сайт позволяет добавить больше 100 единиц.
    """
    inventory = InventoryPage(driver_buyer)
    card = inventory.get_first_card()

    # Пытаемся добавить 105 единиц (заведомо больше лимита)
    for _ in range(105):
        inventory.increase_quantity(card)

    quantity = inventory.get_product_quantity(card)
    assert quantity <= MAX_UNITS_PER_PRODUCT, (
        f"БАГ (ТЗ 2.1): в корзину добавлено {quantity} единиц товара, "
        f"лимит — {MAX_UNITS_PER_PRODUCT}"
    )


def test_max_cart_total(driver_buyer):
    """
    ТЗ 2.2: сумма заказа не должна превышать 100 000 ₽.
    БАГ: сайт не ограничивает сумму.
    """
    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()

    # Ищем самый дорогой товар
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

    # Сколько нужно добавить, чтобы превысить 100 000 ₽
    needed = int(MAX_CART_TOTAL / max_price) + 5
    needed = min(needed, 200)  # ограничим цикл разумным числом

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