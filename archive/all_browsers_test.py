"""
Мультибраузерный тест для Saucedemo.com
Открывает сайт в Google Chrome, Mozilla Firefox и Microsoft Edge
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.firefox import GeckoDriverManager


# Получаем путь к текущей папке
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


def open_chrome(wait_seconds: int = 5) -> bool:
    """
    Открывает сайт в Google Chrome
    
    Args:
        wait_seconds: время ожидания перед закрытием в секундах
    
    Returns:
        bool: True если успешно, False если ошибка
    """
    print("\n" + "="*50)
    print("ЗАПУСК GOOGLE CHROME")
    print("="*50)
    
    try:
        # Chrome не работает с webdriver-manager на вашей системе
        # Используем ручной способ, если драйвер есть
        chrome_driver_path = os.path.join(CURRENT_DIR, "chromedriver.exe")
        
        if os.path.exists(chrome_driver_path):
            print("1. Используем ручной драйвер Chrome")
            service = ChromeService(chrome_driver_path)
        else:
            print("1. Chrome драйвер не найден. Пропускаем Chrome.")
            print("   Скачайте chromedriver.exe с https://chromedriver.chromium.org/")
            return False
        
        print("2. Запуск Google Chrome...")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("3. Открытие сайта: https://www.saucedemo.com/")
        driver.get("https://www.saucedemo.com/")
        
        time.sleep(2)
        print(f"4. Текущий URL: {driver.current_url}")
        
        # Выполняем вход
        print("5. Выполнение входа...")
        username = driver.find_element(By.ID, "user-name")
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.ID, "login-button")
        
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_btn.click()
        
        time.sleep(2)
        print(f"6. URL после входа: {driver.current_url}")
        
        if "inventory" in driver.current_url:
            items = driver.find_elements(By.CLASS_NAME, "inventory_item")
            print(f"7. УСПЕХ: Найдено товаров: {len(items)}")
        else:
            print("7. ОШИБКА: Вход не выполнен")
        
        print(f"\nБраузер закроется через {wait_seconds} секунд...")
        time.sleep(wait_seconds)
        
        driver.quit()
        print("Браузер Chrome закрыт")
        return True
        
    except Exception as error:
        print(f"ОШИБКА при запуске Chrome: {error}")
        return False


def open_firefox(wait_seconds: int = 5) -> bool:
    """
    Открывает сайт в Mozilla Firefox
    
    Args:
        wait_seconds: время ожидания перед закрытием в секундах
    
    Returns:
        bool: True если успешно, False если ошибка
    """
    print("\n" + "="*50)
    print("ЗАПУСК MOZILLA FIREFOX")
    print("="*50)
    
    try:
        print("1. Установка Firefox драйвера...")
        service = FirefoxService(GeckoDriverManager().install())
        
        print("2. Запуск Mozilla Firefox...")
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--start-maximized")
        driver = webdriver.Firefox(service=service, options=firefox_options)
        
        print("3. Открытие сайта: https://www.saucedemo.com/")
        driver.get("https://www.saucedemo.com/")
        
        time.sleep(2)
        print(f"4. Текущий URL: {driver.current_url}")
        
        # Выполняем вход
        print("5. Выполнение входа...")
        username = driver.find_element(By.ID, "user-name")
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.ID, "login-button")
        
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_btn.click()
        
        time.sleep(2)
        print(f"6. URL после входа: {driver.current_url}")
        
        if "inventory" in driver.current_url:
            items = driver.find_elements(By.CLASS_NAME, "inventory_item")
            print(f"7. УСПЕХ: Найдено товаров: {len(items)}")
        else:
            print("7. ОШИБКА: Вход не выполнен")
        
        print(f"\nБраузер закроется через {wait_seconds} секунд...")
        time.sleep(wait_seconds)
        
        driver.quit()
        print("Браузер Firefox закрыт")
        return True
        
    except Exception as error:
        print(f"ОШИБКА при запуске Firefox: {error}")
        return False


def open_edge(wait_seconds: int = 5) -> bool:
    """
    Открывает сайт в Microsoft Edge
    
    Args:
        wait_seconds: время ожидания перед закрытием в секундах
    
    Returns:
        bool: True если успешно, False если ошибка
    """
    print("\n" + "="*50)
    print("ЗАПУСК MICROSOFT EDGE")
    print("="*50)
    
    try:
        # Используем ручной драйвер Edge (уже есть в папке)
        edge_driver_path = os.path.join(CURRENT_DIR, "msedgedriver.exe")
        
        if not os.path.exists(edge_driver_path):
            print("ОШИБКА: Файл msedgedriver.exe не найден!")
            return False
        
        print(f"1. Используем драйвер: {edge_driver_path}")
        
        print("2. Запуск Microsoft Edge...")
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        service = EdgeService(edge_driver_path)
        driver = webdriver.Edge(service=service, options=edge_options)
        
        print("3. Открытие сайта: https://www.saucedemo.com/")
        driver.get("https://www.saucedemo.com/")
        
        time.sleep(2)
        print(f"4. Текущий URL: {driver.current_url}")
        
        # Выполняем вход
        print("5. Выполнение входа...")
        username = driver.find_element(By.ID, "user-name")
        password = driver.find_element(By.ID, "password")
        login_btn = driver.find_element(By.ID, "login-button")
        
        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_btn.click()
        
        time.sleep(2)
        print(f"6. URL после входа: {driver.current_url}")
        
        if "inventory" in driver.current_url:
            items = driver.find_elements(By.CLASS_NAME, "inventory_item")
            print(f"7. УСПЕХ: Найдено товаров: {len(items)}")
        else:
            print("7. ОШИБКА: Вход не выполнен")
        
        print(f"\nБраузер закроется через {wait_seconds} секунд...")
        time.sleep(wait_seconds)
        
        driver.quit()
        print("Браузер Edge закрыт")
        return True
        
    except Exception as error:
        print(f"ОШИБКА при запуске Edge: {error}")
        return False


def run_all_browsers(wait_seconds: int = 5) -> dict:
    """
    Запускает тест во всех браузерах по очереди
    
    Args:
        wait_seconds: время ожидания перед закрытием в секундах
    
    Returns:
        dict: Результаты для каждого браузера
    """
    print("\n" + "="*60)
    print("МУЛЬТИБРАУЗЕРНЫЙ ТЕСТ")
    print("Сайт: https://www.saucedemo.com/")
    print("="*60)
    
    results = {
        "Chrome": open_chrome(wait_seconds),
        "Firefox": open_firefox(wait_seconds),
        "Edge": open_edge(wait_seconds)
    }
    
    # Вывод итогов
    print("\n" + "="*60)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    for browser, success in results.items():
        status = "УСПЕШНО" if success else "НЕ УДАЛОСЬ"
        print(f"{browser:12}: {status}")
    
    successful = sum(1 for success in results.values() if success)
    print(f"\nРезультат: {successful} из 3 браузеров успешно открыли сайт")
    print("="*60)
    
    return results


def run_selected_browser() -> None:
    """
    Интерактивный режим - выбор браузера
    """
    print("\n" + "="*50)
    print("ВЫБОР БРАУЗЕРА")
    print("="*50)
    print("1 - Только Google Chrome")
    print("2 - Только Mozilla Firefox")
    print("3 - Только Microsoft Edge")
    print("4 - Все браузеры")
    
    choice = input("\nВведите номер (1-4): ").strip()
    
    if choice == "1":
        open_chrome()
    elif choice == "2":
        open_firefox()
    elif choice == "3":
        open_edge()
    elif choice == "4":
        run_all_browsers()
    else:
        print("Неверный выбор. Запускаем все браузеры.")
        run_all_browsers()


if __name__ == "__main__":
    """Главная точка входа"""
    run_selected_browser()