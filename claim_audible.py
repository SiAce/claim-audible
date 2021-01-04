import logging

from catergories import categories_names, categories_pages
from cookiesfile import cookies
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait


SUCCESS = '\u2705'
FAIL = '\u274C'
IGNORED = '--'

START_PAGE = 1
END_PAGE = 24
BOOKS_PER_PAGE = 50
WAIT_SECONDS = 10

PLUS_CATALOG_ID = 20956260011


logging.basicConfig(level=logging.INFO)


driver = webdriver.Chrome()

start_url = f"https://www.audible.com/search?audible_programs={PLUS_CATALOG_ID}&sort=popularity-rank&pageSize={BOOKS_PER_PAGE}"
driver.get(start_url)

for cookie in cookies:
    driver.add_cookie(cookie)

for category_id, catergory in categories_names.items():
    catergory_url = f"{start_url}&node={category_id}"
    category_pages = categories_pages[category_id]

    logging.info(f"\nCategory: {catergory}")

    for current_page in range(START_PAGE, category_pages + 1):
        page_url = f"{catergory_url}&page={current_page}"
        driver.get(page_url)

        logging.info(f"Page: {current_page}")

        success_books = []
        fail_books = []

        for book_index in range(BOOKS_PER_PAGE):
            button_xpath = f'//*[@id="adbl-add-to-library-{book_index}"]/div/span/button'

            try:
                button = driver.find_element_by_xpath(button_xpath)

            except:
                continue

            try:
                button = WebDriverWait(driver, WAIT_SECONDS).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button.click()

                success_books.append(book_index)
            except:
                fail_books.append(book_index)

                continue

        logging.info(f"Success: {success_books} {SUCCESS}")
        logging.info(f"Fail: {fail_books} {FAIL}")


driver.close()
