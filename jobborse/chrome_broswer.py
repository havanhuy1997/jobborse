from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.conf import settings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'

class ChromeDriver():
    TIME_TO_WAIT_ELEMENT = 30
    XPATH_TYPE = 'xpath'
    CLASS_TYPE = 'class'
    ID_TYPE = 'id'
    TAG_NAME_TYPE = 'name'

    def __init__(self):
        self.MATCHED_TYPE = {
            self.XPATH_TYPE: By.XPATH,
            self.CLASS_TYPE : By.CLASS_NAME,
            self.ID_TYPE : By.ID,
            self.TAG_NAME_TYPE : By.TAG_NAME    
        }
        prefs = {'profile.managed_default_content_settings.images': 2}
        options = Options()
        options.add_argument(f'user-agent={USER_AGENT}')
        options.add_experimental_option('prefs', prefs)
        options.add_argument("--window-size=1920,1080")

        if not settings.DEVELOP:
            options.add_argument("--start-maximized")
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')  # Last I checked this was necessary.
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        if settings.DEVELOP:
            self.driver = webdriver.Chrome(chrome_options=options)
        else:
            self.driver = webdriver.Chrome('/usr/bin/chromedriver', chrome_options=options)

    def get(self, url):
        self.driver.get(url)

    def _wait_for(self, type, name):
        try:
            element = WebDriverWait(self.driver, self.TIME_TO_WAIT_ELEMENT).until(
                EC.presence_of_element_located((type, name))
            )
        except:
            element = None
            print('Time out for waiting : {}, {}'.format(type, name))
        return element

    def wait_for_class(self, class_name):
        return self._wait_for(By.CLASS_NAME, class_name)

    def wait_for_id(self, id):
        return self._wait_for(By.ID, id)

    def wait_for_xpath(self, xpath):
        return self._wait_for(By.XPATH, xpath)

    def wait_for_clickable(self, type, name):
        try:
            element = WebDriverWait(self.driver, self.TIME_TO_WAIT_ELEMENT).until(
                EC.element_to_be_clickable((self.MATCHED_TYPE[type], name))
            )
        except:
            element = None
            print('Time out to be clickable : {}, {}'.format(type, name))
        return element

    def press_enter(self, element):
        element.send_keys(Keys.ENTER)

    def find_element(self, type, name, from_element=None):
        if not from_element:
            from_element = self.driver
        element = None
        try:
            if type == self.CLASS_TYPE:
                element = from_element.find_element_by_class_name(name)
            elif type == self.ID_TYPE:
                element = from_element.find_element_by_id(name)
            elif type == self.XPATH_TYPE:
                element = from_element.find_element_by_xpath(name)
            elif type == self.TAG_NAME_TYPE:
                element = from_element.find_element_by_tag_name(name)
        except Exception as e:
            print('Error to find element type : {} , {}'.format(type, name))
            print(str(e))
        return element

    def find_elements(self, type, name, from_element=None):
        if not from_element:
            from_element = self.driver
        elements = []
        try:
            if type == self.CLASS_TYPE:
                elements = from_element.find_elements_by_class_name(name)
            elif type == self.ID_TYPE:
                elements = from_element.find_elements_by_id(name)
            elif type == self.XPATH_TYPE:
                elements = from_element.find_elements_by_xpath(name)
            elif type == self.TAG_NAME_TYPE:
                elements = from_element.find_elements_by_tag_name(name)
        except Exception as e:
            print('Error to find elements type : {} , {}'.format(type, name))
            print(str(e))
        return elements

    def scroll_to_element(self, element):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def quite(self):
        self.driver.quit()

    def refresh(self):
        self.driver.refresh()