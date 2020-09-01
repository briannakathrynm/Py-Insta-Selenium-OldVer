import time
from selenium.webdriver.common.by import By


def account_check(driver, account):
    """
    This function will select the account you want to scrape Insights from, while unselecting
    other accounts, if any
    :param driver: Get the current Web session
    :param account: Specified account if there are multiple to scrape from
    :return: None, actions performed on webpage
    """
    # Choose which account to pull from
    chosen_account = account
    accounts_checked = 1
    button = driver.find_element_by_css_selector('#tabHeader > div')
    button.click()
    # Click on selected Account, the time.sleep NEEDS TO BE THERE
    time.sleep(2)
    account_list = []
    accounts = driver.find_elements(By.XPATH, "//div[@class='d1pn00lf cqf1kptm alzwoclg']")
    for acc in accounts:
        acc = acc.text
        account_list.append(acc)
        accounts_checked = accounts_checked + 1
    if chosen_account in account_list:
        # Uncheck every box but Chosen Account...
        check_boxes = driver.find_elements(By.XPATH, "//div[@class='eymtfwi3 c3arhtqu e4ay1f3w rj2hsocd aesu6q9g "
                                                     "s1m0hq7j alzwoclg i85zmo3j']")
        for box in check_boxes:
            checkpoint = box.text.split()[0]
            if checkpoint != chosen_account:
                box = box.click()
        # click on View Button...
        time.sleep(1)
        view = driver.find_element_by_css_selector('#globalContainer > div.uiContextualLayerPositioner.uiLayer > '
                                                   'div > div > div > div > div > div.rj2hsocd.s1m0hq7j.gt60zsk1.'
                                                   'r227ecj6.sl27f92c.alzwoclg.i85zmo3j > div.if5qj5rh.tb4cuiq2.'
                                                   'kojzg8i3')
        view.click()
    else:
        print("Account is not in list, please check the spelling.")
