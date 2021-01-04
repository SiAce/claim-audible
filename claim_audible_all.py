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

driver = webdriver.Chrome()

start_url = f"https://www.audible.com/search?audible_programs=20956260011&feature_six_browse-bin=18685580011&feature_twelve_browse-bin=18685552011&feature_nine_browse-bin=18685524011&sort=popularity-rank&pageSize={BOOKS_PER_PAGE}"
driver.get(start_url)

for cookie in cookies:
    driver.add_cookie(cookie)

for current_page in range(START_PAGE, END_PAGE + 1):
    page_url = f"{start_url}&page={current_page}"
    driver.get(page_url)

    # print(f"Page: {current_page}")

    for book_index in range(BOOKS_PER_PAGE):
        # print(f"{book_index + 1} ", end='', flush=True)

        in_library_xpath = f'//*[@id="adbl-buybox-area-{book_index}"]/div[3]/span/a/span'

        button_xpath = f'//*[@id="adbl-add-to-library-{book_index}"]/div/span/button'

        try:
            button = driver.find_element_by_xpath(button_xpath)
            
        except:
            # print(f"{IGNORED}", end=' ', flush=True)
            continue

        try:
            button = WebDriverWait(driver, WAIT_SECONDS).until(
                EC.element_to_be_clickable((By.XPATH, button_xpath)))
            button.click()

            # print(f"{SUCCESS}", end=' ', flush=True)
        except:
            # print(f"{FAIL}", end=' ', flush=True)

            continue

    # print()


driver.close()
