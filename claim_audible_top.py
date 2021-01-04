from catergories import categories_names
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
END_PAGE = 5
BOOKS_PER_PAGE = 20
WAIT_SECONDS = 10

driver = webdriver.Chrome()

start_url = "https://www.audible.com/most-listened-audiobooks"
driver.get(start_url)

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

for category_id, catergory in categories_names.items():
    print(f"\nCategory: {catergory}")
    
    category_url = f"{start_url}?searchCategory={category_id}&page={START_PAGE}"
    driver.get(category_url)

    for current_page in range(START_PAGE, END_PAGE + 1):
        print(f"Page: {current_page}")

        for book_index in range(BOOKS_PER_PAGE):
            print(f"{book_index} ", end='', flush=True)

            in_library_xpath = f'//*[@id="adbl-buybox-area-{book_index}"]/div[3]/span/a/span'

            try:
                in_library = driver.find_element_by_xpath(in_library_xpath)

                print(f"{IGNORED}", end=' ', flush=True)

                continue
            except:
                pass

            button_xpath = f'//*[@id="adbl-add-to-library-{book_index}"]/div/span/button'

            try:
                button = WebDriverWait(driver, WAIT_SECONDS).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath)))
                button.click()

                print(f"{SUCCESS}", end=' ', flush=True)
            except:
                print(f"{FAIL}", end=' ', flush=True)

                continue
        
        print()

        next_page_link_xpath = f'//*[@id="pagination-a11y-skiplink-target"]/div/div[2]/div/span/ul/li[{current_page + 2}]/a'

        try:
            next_page_link = WebDriverWait(driver, WAIT_SECONDS).until(
                EC.element_to_be_clickable((By.XPATH, next_page_link_xpath)))
            next_page_link.click()
        except:
            break


driver.close()
