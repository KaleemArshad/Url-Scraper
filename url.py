from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import re
from urllib.parse import urlparse
import pandas as pd
import time

driver = webdriver.Chrome(executable_path='C:/WebDrivers/chromedriver.exe')
def scroll(browser, timeout):
    scroll_pause_time = timeout

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            # If heights are the same it will exit the function
            break
        last_height = new_height


driver.maximize_window()
login_url = 'https://www.google.com/'
driver.get(login_url)
driver.implicitly_wait(10)
search_ = 'developer linkedin france'
searchbox_xpath = """//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input"""
find_searchbox = driver.find_element_by_xpath(searchbox_xpath)
find_searchbox.send_keys(search_)
find_searchbox.send_keys(Keys.ENTER)
driver.implicitly_wait(10)
# -------------------------------------------------------PAGE #TILL THE END
url_list = []
try:
    while True:
        driver.implicitly_wait(10)
        scroll(driver, 3)
        src = driver.page_source
        html_soup = bs(src, 'lxml')
        find_link = html_soup.find_all('a')
        for link in find_link:
            get_link = link.get('href')
            try:
                m = re.search("(?P<url>https?://[^\s]+)", get_link)
                n = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if re.search('google.com', domain.netloc):
                    continue
                else:
                    url_list.append(rul)
            except:
                continue

        for url in url_list:
            if url[:11] != 'https://fr.':
                url_list.remove(url)

            else:
                continue

        data = {'URLs': url_list}
        df = pd.DataFrame(data)
        df.to_csv('Url_list.csv')

        next_button_xpath = """//*[@id="pnnext"]/span[2]"""
        find_next = driver.find_element_by_xpath(next_button_xpath)
        find_next.click()
        driver.implicitly_wait(10)


except:
    driver.quit()
    print('No More Pages Found')
