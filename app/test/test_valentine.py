import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

base_url = 'http://awful-valentine.com/'

@pytest.fixture(scope='module')  # фикстура
def driver():
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install()

    )
    yield driver  # "в этой точке будут запускаться все тесты" (открыли драйвер - прошли все тесты - закрыли драйвер)
    # Можно делать как кортеж
    time.sleep(5)
    driver.quit()

def test_slider_image_click_shows_product_page(driver:WebDriver):
    driver.get(base_url)

    featured_title_el  = driver.find_element(By.CSS_SELECTOR, '.featured-title')  #с точки потому что имя класса CSS
    title = featured_title_el.text

    featured_image_el = driver.find_element(By.CSS_SELECTOR, '.featured-image')
    featured_image_el.click()

#Мы нашли название товара, кликнули по нему и проверели совпадает или название новой страницы с названием товара
    assert title in driver.title