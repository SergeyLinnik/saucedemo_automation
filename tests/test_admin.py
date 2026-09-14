import time
from pages.admin_page import AdminPage


def test_admin_sees_product_list(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_manage_page()
    cards = admin.get_product_cards()
    assert len(cards) > 0, "На странице управления нет товаров"


def test_admin_sees_edit_and_delete_buttons(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_manage_page()
    cards = admin.get_product_cards()
    assert len(cards) > 0

    first = cards[0]
    edit_btn = first.find_element(*AdminPage.EDIT_BUTTON)
    delete_btn = first.find_element(*AdminPage.DELETE_BUTTON)
    assert edit_btn.is_enabled(), "Кнопка edit неактивна"
    assert delete_btn.is_enabled(), "Кнопка delete неактивна"


def test_admin_can_open_edit_form(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_manage_page()
    url = admin.click_edit_first_product()
    assert "/editProduct/" in url, f"Не перешли на форму редактирования: {url}"
    name = admin.get_name()
    assert name != "", "Поле 'Наименование' пустое"


def test_admin_can_change_name_in_form(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_manage_page()
    admin.click_edit_first_product()

    original = admin.get_name()
    assert original, "Не удалось прочитать название"

    new_name = original + " TEST"
    admin.set_name(new_name)
    time.sleep(0.5)
    assert admin.get_name() == new_name


def test_admin_can_open_create_form(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_manage_page()
    url = admin.click_add_product()
    assert "/createProduct" in url, f"Не перешли на форму создания: {url}"

    # Проверяем только те поля, которые точно есть (по скриншотам)
    assert admin.find_element(AdminPage.NAME_INPUT) is not None
    assert admin.find_element(AdminPage.DESCRIPTION_INPUT) is not None
    assert admin.find_element(AdminPage.EXPECTED_CATEGORY_INPUT) is not None
    assert admin.find_element(AdminPage.PRICE_INPUT) is not None
    assert admin.find_element(AdminPage.IMAGE_INPUT) is not None


def test_empty_form_shows_validation(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_create_page()

    assert not admin.is_create_button_enabled(), \
        "Кнопка 'Создать товар' должна быть disabled при пустой форме"
    invalid_count = admin.count_invalid_fields()
    assert invalid_count > 0, "Пустая форма не помечает поля как .is-invalid"


def test_form_enables_create_button_after_filling(driver_admin):
    admin = AdminPage(driver_admin)
    admin.open_create_page()

    admin.fill_full_form(
        name="Автотест товар",
        desc="Описание для теста",
        expected_cat="Тестовая",
        cat="Тест",
        price=999,
        image="http://example.com/image.jpg"
    )
    time.sleep(1)
    assert admin.is_create_button_enabled(), \
        "Кнопка 'Создать товар' осталась disabled после заполнения полей"