import json
import time

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='module')  # фикстура
def driver():
    driver = webdriver.Chrome(
        executable_path=ChromeDriverManager().install()

    )
    yield driver  # "в этой точке будут запускаться все тесты" (открыли драйвер - прошли все тесты - закрыли драйвер)
    # Можно делать как кортеж
    time.sleep(5)
    driver.quit()


@pytest.fixture(scope='module')  # создали фикстуру чтобы с помощью ее брать данные из env в папке env
def environment():
    env = json.load(open('./env/env.json'))
    return env['test']


def test_slider_first_image_click_shows_product_page(driver: WebDriver, environment):
    base_url = environment['base_url']
    driver.get(base_url)

    # Ничего не оптимизируйте, пока в этом нет необходимости
    featured_title_el = driver.find_element(By.CSS_SELECTOR, '.featured-title')  # с точки потому что имя класса CSS
    title = featured_title_el.text

    featured_image_el = driver.find_element(By.CSS_SELECTOR, '.featured-image')
    featured_image_el.click()

    # Мы нашли название товара, кликнули по нему и проверели совпадает или название новой страницы с названием товара
    assert title in driver.title
    category_title_el = driver.find_element(By.CSS_SELECTOR, '.category-title')
    assert title == category_title_el.text

    driver.save_screenshot('./screenshot.png')  # создается скриншот. Обновляется после каждого теста


def test_slider_second_image_click_shows_product_page(driver: WebDriver, environment):
    goto_homepage(driver, environment)
    select_slide(driver, 2)
    slide_info = get_slide_info(driver, 2)
    click_slide_image(driver, 2)

    # NoSuchElementException: элемент на странице не найден
    # ElementNotVisibleException: элемент не видим, взаимодействовать (кликать) с ним нельзя
    # ReferenceStalenessException: сначала нашли, а потом он исчез

    assert slide_info['title'] in driver.title
    category_info = get_category_info(driver)
    assert slide_info['title'] == category_info['title']


def goto_homepage(driver, environment):
    base_url = environment['base_url']
    driver.get(base_url)


def select_slide(driver, slide_no):
    slide_handle_el = driver.find_elements(
        By.CSS_SELECTOR, '#controllers > a'
    )[slide_no - 1]

    slide_handle_el.click()


def get_slide_info(driver, slide_no):
    info = {}  # создаём пустой dict
    slide_el = driver.find_elements(
        By.CSS_SELECTOR, '.slide'
    )[slide_no - 1]

    featured_title_el = slide_el.find_element(
        By.CSS_SELECTOR, '.featured-title'
    )
    info['title'] = featured_title_el.text

    price_el = slide_el.find_element(
        By.CSS_SELECTOR, '.price'
    )
    info['price'] = price_el.text

    return info


def click_slide_image(driver, slide_no):
    featured_image_el = driver.find_elements(
        By.CSS_SELECTOR, '.featured-image'
    )[slide_no - 1]
    featured_image_el.click()


def get_category_info(driver):
    info = {}
    category_title_el = driver.find_element(By.CSS_SELECTOR, '.category-title')
    info['title'] = category_title_el.text
    return info