from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time

@pytest.fixture
def driver():
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()

def test_laravel_login_and_navigation(driver):
    # 1. Авторизация
    driver.get("https://svetlanadracheva.ru/login")

    driver.find_element(By.NAME, "identity").send_keys("cj@cj.com")
    driver.find_element(By.NAME, "password").send_keys("cj")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    # 2. Ждём загрузку бокового меню
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "nav-sidebar"))
    )

    # 3. Переход по всем ссылкам навигации
    nav_links = driver.find_elements(By.CSS_SELECTOR, ".nav-sidebar a.nav-link")
    hrefs = [link.get_attribute("href") for link in nav_links if link.get_attribute("href")]

    for href in hrefs:
        driver.get(href)
        print(f"Перешли по ссылке: {href}")
        assert href in driver.current_url or driver.current_url.startswith(href)

    # 4. Переход на главную через логотип
    logo_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[h4[contains(text(), 'Название')]]"))
    )
    logo_link.click()

    # 5. Ждём загрузку календаря
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "calendar"))
    )

    # 6. Клик по событию в календаре (если есть хотя бы одно)
    try:
        event = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-event.fc-event-start.fc-event-end"))
        )
        event_href = event.get_attribute("href")
        print(f"Клик по событию: {event_href}")
        event.click()
    except:
        print("Событие в календаре не найдено — продолжаем")

    # 7. Переход снова на главную через логотип
    logo_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[h4[contains(text(), 'Название')]]"))
    )
    logo_link.click()

    # 8. Повторно ждём загрузку календаря
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "calendar"))
    )

    # 9. Два клика по кнопке "следующий месяц"
    for i in range(2):
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "fc-next-button"))
        )
        next_button.click()
        print(f"Клик по переключателю месяца №{i + 1}")
