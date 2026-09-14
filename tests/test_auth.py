from pages.login_page import LoginPage
import time


def test_login_buyer(driver):
    """Тест на успешную авторизацию под ролью Покупатель (кириллица)"""
    login_page = LoginPage(driver)
    # Используем покупатель1, чтобы не засорять корзину основного покупателя
    login_page.login("покупатель1", "покупатель1")
    time.sleep(2)
    assert "login" not in driver.current_url.lower(), "Не удалось авторизоваться!"


def test_login_admin(driver):
    """Тест на успешную авторизацию под ролью Админ"""
    login_page = LoginPage(driver)
    login_page.login("admin", "admin")
    time.sleep(2)
    assert "login" not in driver.current_url.lower(), "Не удалось авторизоваться под админом!"