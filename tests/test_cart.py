from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
import time


def test_add_to_cart(driver_buyer):
    """Добавление товара в корзину и увеличение счётчика"""
    inventory = InventoryPage(driver_buyer)
    counter_before = inventory.get_cart_counter()

    cards = inventory.get_product_cards()
    assert len(cards) > 0, "На странице нет товаров"

    inventory.increase_quantity(cards[0])
    counter_after = inventory.get_cart_counter()

    assert counter_after > counter_before, \
        f"Счётчик не вырос: было {counter_before}, стало {counter_after}"


def test_cart_contains_item(driver_buyer):
    """Товар появляется в корзине после добавления"""
    inventory = InventoryPage(driver_buyer)
    cards = inventory.get_product_cards()
    name = inventory.get_product_name(cards[0])
    inventory.increase_quantity(cards[0])

    inventory.open_cart()
    cart = CartPage(driver_buyer)
    items = cart.get_cart_items()
    assert len(items) > 0, "Корзина пуста после добавления"

    names = [cart.get_item_name(i) for i in items]
    assert name in names, f"Товар '{name}' не найден в корзине. Есть: {names}"


def test_cart_total(driver_buyer):
    """Итоговая сумма > 0"""
    inventory = InventoryPage(driver_buyer)
    inventory.increase_quantity(inventory.get_product_cards()[0])
    inventory.open_cart()
    cart = CartPage(driver_buyer)
    total = cart.get_total_price()
    assert total > 0, "Итоговая сумма равна 0"


def test_checkout_button_exists(driver_buyer):
    """Кнопка 'Оформить заказ' есть и активна"""
    inventory = InventoryPage(driver_buyer)
    inventory.increase_quantity(inventory.get_product_cards()[0])
    inventory.open_cart()
    cart = CartPage(driver_buyer)
    button = cart.find_element(CartPage.CHECKOUT_BUTTON)
    assert button.is_enabled(), "Кнопка 'Оформить заказ' неактивна"


def test_clear_cart(driver_buyer):
    """Уменьшение количества товара до 0 удаляет его из корзины"""
    inventory = InventoryPage(driver_buyer)
    inventory.increase_quantity(inventory.get_product_cards()[0])
    inventory.open_cart()

    cart = CartPage(driver_buyer)
    items_before = cart.get_cart_items()
    assert len(items_before) > 0, "Корзина пуста, нечего удалять"

    # Обнуляем количество первого товара
    card = items_before[0]
    qty = cart.get_item_quantity(card)
    for _ in range(qty):
        cart.decrease_quantity(card)

    time.sleep(2)
    items_after = cart.get_cart_items()
    assert len(items_after) < len(items_before), \
        f"Товар не удалился. Было {len(items_before)}, стало {len(items_after)}"