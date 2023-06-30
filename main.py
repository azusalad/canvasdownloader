from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import os
from tqdm import tqdm
from config import *

def create_driver(download_dir):
    """Create geckodriver given a path and ublock origin xpi file (optional)"""

    # get mime types
    with open('../mimetypes.txt','r') as f:
        mime_types = ';'.join(x.strip() for x in f.readlines() if x != '')

    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.downloadDir", download_dir)
    options.set_preference("browser.download.defaultFolder", download_dir)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
    options.set_preference("pdfjs.disabled",True)
    options.headless = False
    print('creating driver')
    service = Service(executable_path=gecko_path)
    driver = webdriver.Firefox(options=options, service=service)
    try:
        driver.install_addon(os.path.join(os.getcwd(), ublock_path), temporary=True)
    except:
        print('Cannot install ublock origin, skipping')
    return driver

def set_symlink(course):
    """Create a symlink that points to the course download location.  So firefox download path does not need to change"""
    # https://stackoverflow.com/questions/31734447/changing-firefoxprofile-preferences-more-than-once-using-selenium-python
    if os.path.exists('symlink'):
        # remove symlink folder if it exists
        try:
            os.rmdir('symlink') # if it is regular directory
        except:
            os.unlink('symlink') # if it is symlink
    os.mkdir(str(course))
    os.symlink(str(course), 'symlink')

def expand(driver):
    """Expand all modules"""
    driver.find_element(By.CSS_SELECTOR,'#expand_collapse_all').click()
    if driver.find_element(By.CSS_SELECTOR,'#expand_collapse_all').text == 'Expand All':
        driver.find_element(By.CSS_SELECTOR,'#expand_collapse_all').click()

def download(driver,href):
    """Downloads the attachment from the module href"""
    driver.get(href)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div:nth-child(2) > span:nth-child(1) > a:nth-child(1)'))).click()
    time.sleep(cooldown)

def log(course,href,msg):
    with open('log.txt','a') as f:
        f.write(f"{msg} {course} {href}\n")

# go into downloads folder and create a driver
os.chdir('downloads')
absolute_path = os.getcwd()
driver = create_driver(os.path.join(str(absolute_path), 'symlink'))
driver.get(canvas_url)
input('Press enter once you have finished logging in and loaded the next page')

for course in course_ids:
    set_symlink(course)
    driver.get(f"{canvas_url}courses/{course}/modules/")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#expand_collapse_all')))
    # expand all modules
    expand(driver)
    # find modules
    content = driver.find_element(By.ID,'context_modules')
    modules = content.find_elements(By.TAG_NAME,"li")
    # get hrefs of all modules that have an attachment
    hrefs = []
    print('Finding appropriate modules')
    for module in tqdm(modules):
        if module.find_element(By.CLASS_NAME,'screenreader-only').text == 'Attachment':
            hrefs.append(module.find_element(By.TAG_NAME,'a').get_attribute('href'))
    # Iterate through hrefs and download
    for href in tqdm(hrefs):
        log(course,href,'fetching')
        download(driver, href)
        log(course,href,'downloaded')

driver.close()
