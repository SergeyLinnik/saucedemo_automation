from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
import time

print("=" * 50)
print("ЗАПУСК АВТОМАТИЗИРОВАННОГО ТЕСТА")
print("=" * 50)

try:
    # 1. Запускаем Firefox
    print("\n1. Запуск Firefox...")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service)
    print("[OK] Firefox успешно запущен")

    # 2. Открываем сайт
    print("\n2. Открытие сайта Saucedemo...")
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    print("[OK] Сайт загружен")
    time.sleep(1)

    # 3. Находим элементы на странице
    print("\n3. Поиск элементов на странице...")
    username_field = driver.find_element(By.ID, "user-name")
    password_field = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "login-button")
    print("[OK] Все элементы найдены")

    # 4. Вводим логин
    print("\n4. Ввод логина...")
    username_field.send_keys("standard_user")
    print("[OK] Логин введен: standard_user")

    # 5. Вводим пароль
    print("\n5. Ввод пароля...")
    password_field.send_keys("secret_sauce")
    print("[OK] Пароль введен: secret_sauce")

    time.sleep(1)

    # 6. Нажимаем кнопку Login
    print("\n6. Нажатие кнопки Login...")
    login_button.click()
    print("[OK] Кнопка нажата")

    # 7. Проверяем результат
    time.sleep(2)
    print("\n7. Проверка результата...")
    
    if "inventory.html" in driver.current_url:
        print("=" * 50)
        print("[SUCCESS] ТЕСТ ПРОЙДЕН УСПЕШНО")
        print("=" * 50)
        print(f"[INFO] Текущий URL: {driver.current_url}")
        print("[INFO] Вы успешно вошли в систему")
        
        # Получаем заголовок страницы
        title = driver.title
        print(f"[INFO] Заголовок страницы: {title}")
        
        # Считаем количество товаров
        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        print(f"[INFO] Найдено товаров: {len(items)}")
        
    else:
        print(f"[ERROR] Ошибка! Текущий URL: {driver.current_url}")
        print("[ERROR] Проверьте правильность ввода данных")

    # 8. Оставляем браузер открытым для просмотра
    print("\n8. Браузер закроется через 10 секунд...")
    print("[INFO] Посмотрите результат в открывшемся окне Firefox")
    time.sleep(10)

except Exception as e:
    print(f"\n[ERROR] Произошла ошибка: {e}")
    print("\nВозможные причины:")
    print("- Не установлен Firefox браузер")
    print("- Нет интернет-соединения")
    print("- Проблемы с драйвером")

finally:
    # Закрываем браузер
    print("\n[INFO] Закрытие браузера...")
    driver.quit()
    print("[OK] Тест завершен. Браузер закрыт.")

print("\n" + "=" * 50)
print("ПРОГРАММА ЗАВЕРШЕНА")
print("=" * 50)