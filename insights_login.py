from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class Login:
    def __init__(self, driver, username, password, two_fact_code):
        self.driver = driver
        self.username = username
        self.password = password
        self.two_fact_code = two_fact_code

    def sign_in(self):
        """
        Function that signs in automatically into Creator Studio with a specified username and password.
        Variables:
        Self: self
        :return: None, opens an instance of Chrome and automatically logs in.
        """
        try:
            self.driver.get('https://business.facebook.com/creatorstudio/')
            # Clicks on first "Facebook Login Button"
            button = self.driver.find_element_by_css_selector(
                '#u_0_0 > div.i85zmo3j.alzwoclg.kfcdz00w.jcxyg2ei.om3e55n1.mfclru0v > div > '
                'div.fefz03bc > div > div > div > div:nth-child(2) > div > div > span > div > div > div')
            button.click()

            # Looks for username in a specific amount of time, enough for webpage to load
            user_id = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                           '#email')))
            user_id.click()
            user_id.send_keys(self.username)

            # Looks for password in a specific amount of time, enough for webpage to load
            pwd = self.driver.find_element_by_css_selector(
                '#pass')
            pwd.click()
            pwd.send_keys(self.password)

            # Clicks on Login Button
            button = self.driver.find_element_by_css_selector(
                '#loginbutton')
            button.click()

            if self.two_fact_code is not None:
                login_code = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                                  '#approvals_code')))
                login_code.click()
                login_code.send_keys(self.two_fact_code)
                button = self.driver.find_element_by_css_selector('#checkpointSubmitButton')
                button.click()
        except NoSuchElementException:
            # Looks for username in a specific amount of time, enough for webpage to load
            user_id = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                 '#email')))
            user_id.click()
            user_id.send_keys(self.username)

            # Looks for password in a specific amount of time, enough for webpage to load
            pwd = self.driver.find_element_by_css_selector(
                '#pass')
            pwd.click()
            pwd.send_keys(self.password)

            # Clicks on Login Button
            button = self.driver.find_element_by_css_selector(
                '#loginbutton')
            button.click()
