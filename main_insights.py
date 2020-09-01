from selenium import webdriver
from InsightsCopy import insights_login
from InsightsCopy import insights_details
import os

# THIS IS THE PART YOU ONLY NEED TO ENTER INFORMATION IN
driver = 0
username = "inkyheart@earthlink.net"    # Username of account (Instagram or Facebook Username)
password = "M@cb1g2k2ohmy"              # Password of account (Instagram or Facebook Password)
two_fact_code = None                    # Enter Backup Code of account if 2Fact for Instagram, set to NONE if otherwise
post_count = 30                         # Number of posts you want the insights on
mode = "Photos"                         # Enter what type of posts you want to get Insights on
account = "sketchbookskool"             # Enter which account (if any) that you want to specify

# For mode, choose the following: Photos, Videos


def main():
    global driver
    # Makes directory to hold image files
    os.mkdir("C://Users/Brianna's HP17/Desktop/post_extraction")
    print("Running...")
    # The below line of code will create an instance of Chrome using selenium
    driver = webdriver.Chrome("C://Users/Brianna's HP17/Desktop/chromedriver.exe")
    driver.delete_all_cookies()
    # Logging in to selected profile...
    print("Logging In...")
    log = insights_login.Login(driver, username, password, two_fact_code)
    log.sign_in()
    # Navigate to Instagram Insights
    print("Navigating...")
    insights_details.navigate(driver)
    # Getting Insights for Posts
    print("Getting Insights...")
    insights_details.posts(driver, post_count, mode, account)


if __name__ == '__main__':
    main()
