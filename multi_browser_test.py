"""
Мультибраузерный тест для Saucedemo.com
Открывает сайт в Chrome, Firefox и Microsoft Edge
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def open_chrome(wait_seconds: int = 3) -> bool:
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
        print("1. Установка Chrome драйвера...")
        service = ChromeService(ChromeDriverManager().install())
        
        print("2. Запуск Google Chrome...")
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("3. Открытие сайта: https://www.saucedemo.com/")
        driver.get("https://www.saucedemo.com/")
        
        time.sleep(2)
        print(f"4. Текущий URL: {driver.current_url}")
        print("5. УСПЕХ: Сайт успешно загружен в Chrome")
        
        print(f"\nБраузер закроется через {wait_seconds} секунд...")
        time.sleep(wait_seconds)
        
        driver.quit()
        print("Браузер Chrome закрыт")
        return True
        
    except Exception as error:
        print(f"ОШИБКА при запуске Chrome: {error}")
        return False


def open_firefox(wait_seconds: int = 3) -> bool:
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
        print("5. УСПЕХ: Сайт успешно загружен в Firefox")
        
        print(f"\nБраузер закроется через {wait_seconds} секунд...")
        time.sleep(wait_seconds)
        
        driver.quit()
        print("Браузер Firefox закрыт")
        return True
        
    except Exception as error:
        print(f"ОШИБКА при запуске Firefox: {error}")
        return False


def open_edge(wait_seconds: int = 3) -> bool:
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
        print("1. Установка Edge драйвера...")
        service = EdgeService(EdgeChromiumDriverManager().install())
        
        print("2. Запуск Microsoft Edge...")
        edge_options = EdgeOptions()
        edge_options.add_argument("--start-maximized")
        driver = webdriver.Edge(service=service, options=edge_options)
        
        print("3. Открытие сайта: https://www.saucedemo.com/")
        driver.get("https://www.saucedemo.com/")
        
        time.sleep(2)
        print(f"4. Текущий URL: {driver.current_url}")
        print("5. УСПЕХ: Сайт успешно загружен в Edge")
        
        print(f"\nБраузер закроется через {wait_seconds} секунд...")
        time.sleep(wait_seconds)
        
        driver.quit()
        print("Браузер Edge закрыт")
        return True
        
    except Exception as error:
        print(f"ОШИБКА при запуске Edge: {error}")
        return False


def run_all_browsers(wait_seconds: int = 3) -> dict:
    """
    Запускает тест во всех браузерах
    
    Args:
        wait_seconds: время ожидания перед закрытием в секундах
    
    Returns:
        dict: Результаты для каждого браузера
    """
    print("\n" + "="*60)
    print("ЗАПУСК МУЛЬТИБРАУЗЕРНОГО ТЕСТА")
    print("Сайт: https://www.saucedemo.com/")
    print("="*60)
    
    results = {}
    
    results["Chrome"] = open_chrome(wait_seconds)
    results["Firefox"] = open_firefox(wait_seconds)
    results["Edge"] = open_edge(wait_seconds)
    
    # Вывод итогов
    print("\n" + "="*60)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    for browser, success in results.items():
        status = "УСПЕШНО" if success else "НЕ УДАЛОСЬ"
        print(f"{browser:12}: {status}")
    
    successful = sum(1 for success in results.values() if success)
    print(f"Результат: {successful} из 3 браузеров успешно открыли сайт")
    print("="*60)
    
    return results


def run_single_browser() -> None:
    """
    Интерактивный режим - выбор одного браузера
    """
    print("\n" + "="*50)
    print("ВЫБОР БРАУЗЕРА")
    print("="*50)
    print("1 - Google Chrome")
    print("2 - Mozilla Firefox")
    print("3 - Microsoft Edge")
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


# Точка входа в программу
if __name__ == "__main__":
    """
    Главная функция, которая запускается при выполнении скрипта
    """
    run_single_browser()