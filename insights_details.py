import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from InsightsCopy import insights_images
from InsightsCopy import insights_accounts
from selenium.common.exceptions import NoSuchElementException


def navigate(driver):
    """
    This function will navigate to Instagram Insights from the Business Facebook
    Creator Studio
    :param driver: Takes the same Selenium session from previous program
    :return: None, opens Instagram insights
    """
    time.sleep(5)
    # Clicks on Instagram Button
    button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#media_manager_chrome_'
                                                                                              'bar_instagram_icon')))
    button.click()


def posts(driver, post_count, mode, account):
    """
    This function will take a number of posts desired, and gather the post links
    :param driver: Takes the same Selenium session from previous program
    :param post_count: Number of desired posts from the Instagram account
    :param mode: Specify what type of posts to get Insights from
    :param account: Specify what account to get Insights from, if any
    :return: None
    """

    # Wait for posts page to load
    WebDriverWait(driver, 10).until((EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                     '#u_0_1 > div > div:nth-child(2) > '
                                                                     'div:nth-child(1) > div.gxrezr7k.m8h3af8h.'
                                                                     'prip0d9i.kjdc1dyq.ke3z0m61.rq3p4edu.lq84ybu9.'
                                                                     'om3e55n1.riryi2nx.qgpwno1r.rl78xhln.ajm2t2ys.'
                                                                     'e1bfhk1b > div > div.aglvbi8b > div.i0rxk2l3'))))
    time.sleep(5)

    # First, identify the type of post to grab Insights from
    if mode == "Photos":
        photo_url = "https://business.facebook.com/creatorstudio/?tab=instagram_content_posts&mode=instagram&content_" \
                    "table=INSTAGRAM_PHOTO_POSTS#"
        driver.get(photo_url)
        time.sleep(5)
        insights_accounts.account_check(driver, account)

        details = pd.DataFrame([])
        for post_num in range(post_count):
            time.sleep(5)
            post_num = post_num + 1
            post_loc = post_num - 1
            style_width = str(40 + 88 * post_loc)
            scroll_bar = driver.find_element_by_css_selector('#js_2w > div > div > div > div:nth-child(1) > div > div '
                                                             '> div.ReactVirtualized__Grid._1zmk > div')
            scroll_bar.send_keys(Keys.ARROW_DOWN)
            element = WebDriverWait(driver, 10) \
                .until((EC.presence_of_element_located((By.XPATH, "//div[@class='_2e42 _2yi0 _2yia']"
                                                                  "[@style='height: 88px; left: 62px; position: "
                                                                  "absolute; top: {}px; width: 420px; "
                                                                  "background-color: transparent; border-color:"
                                                                  " rgb(221, 223, 226);']".format(style_width)))))
            driver.execute_script("arguments[0].scrollIntoView();", element)
            driver.implicitly_wait(2)
            element.click()

            # Grabbing Post Info...
            post_info = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj '
                '> div._759f > div > div._75fm > div > p > span').text

            # Grabbing Interactions...
            time.sleep(1)
            interactions = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj > div._759g > div._76la._76l6 > '
                'div:nth-child(2) > div > span.l61y9joe.guf7j0zz.f8t1w9yb.jcd5tngi.svz86pwt.jrvjs1jy.a53abz89').text

            # Grabbing Percentage not Following:
            percentage = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > div > div._'
                                                             '75fj > div._759g > div._76la._76l6 > div:nth-child(2) > '
                                                             'div > span:nth-child(3)').text.split()[0]
            percentage = (percentage.rstrip("%"))

            # Grabbing Follows...
            follows = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj '
                '> div._759g > div._76la._76l6 > div._76l9._3-8z > div > '
                'div.l61y9joe.o4zun6ui.pf8wtfb4.jcd5tngi.kiex77na.lgsfgr3h.'
                'mcogi7i5.ih1xi9zn.jrvjs1jy.a53abz89').text

            # Grabbing Reach...
            reach = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj > div._759g'
                ' > div._76la._76l6 > div:nth-child(4) > div > div.l61y9joe.o4zun6ui.'
                'pf8wtfb4.jcd5tngi.kiex77na.lgsfgr3h.mcogi7i5.ih1xi9zn.jrvjs1jy.a53ab'
                'z89').text

            # Grabbing Impressions...
            impressions = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj > '
                'div._759g > div._76la._76l6 > div:nth-child(5) > div._3qn7._'
                '61-3._2fyi._3qng > div.l61y9joe.o4zun6ui.pf8wtfb4.jcd5tngi.'
                'kiex77na.lgsfgr3h.mcogi7i5.ih1xi9zn.jrvjs1jy.a53abz89').text

            # Setting Initial Values
            impressions_profile = str(0)
            impressions_explore = str(0)
            impressions_hashtags = str(0)

            if impressions == str(0):
                impressions_home = str(0)
            else:
                try:
                    impressions_home = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:nth-'
                        'child(5) > div:nth-child(2) > div > div:nth-'
                        'child(2)')
                    impressions_home = impressions_home.text
                except NoSuchElementException:
                    print("Element not found, setting to 0.")
                    impressions_home = str(0)

            # Checking what Impression we have in position 5-3-1...
            try:
                impressions_check = driver.find_element_by_css_selector(
                    '#creator_studio_sliding_tray_root > div > '
                    'div > div._75fj > div._759g > div._76la._76l6'
                    ' > div:nth-child(5) > div:nth-child(3) > div >'
                    ' div:nth-child(1)').text
            except NoSuchElementException:
                impressions_check = None

            try:
                if impressions_check == "From Profile":
                    impressions_profile = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(3) > div > div:'
                        'nth-child(2)')
                    impressions_profile = impressions_profile.text
                    impressions_explore = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_profile = str(0)

            try:
                if impressions_check == "From Explore":
                    impressions_explore = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(3) > div > div:'
                        'nth-child(2)')
                    impressions_explore = impressions_explore.text
                    impressions_profile = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_explore = str(0)

            try:
                if impressions_check == "From Hashtags":
                    impressions_hashtags = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div '
                        '> div._75fj > div._759g > div._76la._76l6 > '
                        'div:nth-child(5) > div:nth-child(3) > div > '
                        'div:nth-child(2)')
                    impressions_hashtags = impressions_hashtags.text
            except NoSuchElementException:
                print("Element not found, setting to 0.")
                impressions_hashtags = str(0)

            # Checking what Impression we have in position 5-4-1...
            try:
                impressions_check = driver.find_element_by_css_selector(
                    '#creator_studio_sliding_tray_root > div > '
                    'div > div._75fj > div._759g > div._76la._76l6'
                    ' > div:nth-child(5) > div:nth-child(4) > div >'
                    ' div:nth-child(1)').text
            except NoSuchElementException:
                impressions_check = None

            try:
                if impressions_check == "From Profile":
                    impressions_profile = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(4) > div > div:'
                        'nth-child(2)')
                    impressions_profile = impressions_profile.text
                    impressions_explore = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_profile = str(0)

            try:
                if impressions_check == "From Explore":
                    impressions_explore = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(4) > div > div:'
                        'nth-child(2)')
                    impressions_explore = impressions_explore.text
                    impressions_profile = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_explore = str(0)

            try:
                if impressions_check == "From Hashtags":
                    impressions_hashtags = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div '
                        '> div._75fj > div._759g > div._76la._76l6 > '
                        'div:nth-child(5) > div:nth-child(4) > div > '
                        'div:nth-child(2)')
                    impressions_hashtags = impressions_hashtags.text
            except NoSuchElementException:
                print("Element not found, setting to 0.")
                impressions_hashtags = str(0)

            try:
                impressions_other = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > '
                                                                        'div > div > div._75fj > div._759g > '
                                                                        'div._76la._76l6 > div:nth-child(5) > '
                                                                        'div:nth-child(5) > div > div:nth-'
                                                                        'child(2)')
                impressions_other = impressions_other.text
            except NoSuchElementException:
                print("Element not found, setting to 0.")
                impressions_other = str(0)

            # Getting the Image from the Post...
            image = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > div > div._75fj '
                                                        '>div._759f > div > div._8oy2 > div > img')

            image_url = image.get_attribute("src")

            # Getting Images from URL...
            insights_images.url_to_img(url=image_url, filename="insta_post" + str(post_num) + ".jpg")

            # Compiling Insight Findings...
            insight_details = {'image url': image_url, 'post info': post_info, 'interactions': interactions,
                               'percentage not following': percentage, 'follows': follows, 'reach': reach,
                               'impressions': impressions, 'from home': impressions_home,
                               'from hashtags': impressions_hashtags, 'from profile': impressions_profile,
                               'from explore': impressions_explore, 'from other': impressions_other}

            # Creating DataFrame
            post_details = pd.DataFrame(insight_details, index=[0])
            details = details.append(post_details, ignore_index=True)

            # Return to Main Post Page
            time.sleep(2)
            go_back = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > '
                                                          'div > div:nth-child(1) > div._6n_t')
            go_back.click()

            # Program Finished...
            if post_num == post_count:
                # Exports all Details to a CSV file at the following path:
                details.to_csv("C://Users/Brianna's HP17/Desktop/overall_details_csv " + mode + ".csv")

    if mode == "Videos":
        video_url = "https://business.facebook.com/creatorstudio/?tab=instagram_content_posts&mode=instagram&content_" \
                    "table=INSTAGRAM_VIDEO_POSTS#"
        driver.get(video_url)
        time.sleep(10)
        post_num = 0
        insights_accounts.account_check(driver, account)

        details = pd.DataFrame([])
        for post_num in range(post_count):
            time.sleep(3)
            post_num = post_num + 1
            post_loc = post_num - 1
            style_width = str(40 + 88 * post_loc)
            element = driver.find_element(By.XPATH,
                                          "//div[@class='_2e42 _2yi0 _2yia'][@style='height: 88px; left: 62px; "
                                          "position: absolute; top: {}px; width: 420px; background-color: transparent; "
                                          "border-color: rgb(221, 223, 226);']".format(
                                              style_width))
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            time.sleep(3)

            # Grabbing Views...
            views = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > div > div._75fj'
                                                        ' > div._759g > div._7hf9._76l6 > div._3-8z > div > div.l'
                                                        '61y9joe.o4zun6ui.pf8wtfb4.jcd5tngi.kiex77na.lgsfgr3h.'
                                                        'mcogi7i5.ih1xi9zn.jrvjs1jy.a53abz89').text

            # Grabbing Interactions...
            interactions = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj > div._759g > div:nth-child(3) > '
                'div:nth-child(2) > div > span.l61y9joe.guf7j0zz.f8t1w9yb.jcd5tngi.svz86pwt.jrvjs1jy.a53abz89').text

            # Grabbing Percentage not Following:
            percentage = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > div > '
                                                             'div._75fj > div._759g > div._76la._76l6 > div:nth'
                                                             '-child(2) > div > span:nth-child(3)').text
            percentage = (percentage.rstrip("%"))

            # Grabbing Follows...
            follows = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj '
                '> div._759g > div._76la._76l6 > div._76l9._3-8z > div > '
                'div.l61y9joe.o4zun6ui.pf8wtfb4.jcd5tngi.kiex77na.lgsfgr3h.'
                'mcogi7i5.ih1xi9zn.jrvjs1jy.a53abz89').text

            # Grabbing Reach...
            reach = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj > div._759g'
                ' > div._76la._76l6 > div:nth-child(4) > div > div.l61y9joe.o4zun6ui.'
                'pf8wtfb4.jcd5tngi.kiex77na.lgsfgr3h.mcogi7i5.ih1xi9zn.jrvjs1jy.a53ab'
                'z89').text

            # Grabbing Impressions...
            impressions = driver.find_element_by_css_selector(
                '#creator_studio_sliding_tray_root > div > div > div._75fj > '
                'div._759g > div._76la._76l6 > div:nth-child(5) > div._3qn7._'
                '61-3._2fyi._3qng > div.l61y9joe.o4zun6ui.pf8wtfb4.jcd5tngi.'
                'kiex77na.lgsfgr3h.mcogi7i5.ih1xi9zn.jrvjs1jy.a53abz89').text

            # Setting Initial Values
            impressions_profile = str(0)
            impressions_explore = str(0)
            impressions_hashtags = str(0)

            if impressions == str(0):
                impressions_home = str(0)
            else:
                try:
                    impressions_home = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:nth-'
                        'child(5) > div:nth-child(2) > div > div:nth-'
                        'child(2)')
                    impressions_home = impressions_home.text
                except NoSuchElementException:
                    print("Element not found, setting to 0.")
                    impressions_home = str(0)

            # Checking what Impression we have in position 5-3-1...
            try:
                impressions_check = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > '
                                                                        'div > div._75fj > div._759g > div._76la._76l6'
                                                                        ' > div:nth-child(5) > div:nth-child(3) > div >'
                                                                        ' div:nth-child(1)').text
            except NoSuchElementException:
                impressions_check = None

            try:
                if impressions_check == "From Profile":
                    impressions_profile = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(3) > div > div:'
                        'nth-child(2)')
                    impressions_profile = impressions_profile.text
                    impressions_explore = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_profile = str(0)

            try:
                if impressions_check == "From Explore":
                    impressions_explore = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(3) > div > div:'
                        'nth-child(2)')
                    impressions_explore = impressions_explore.text
                    impressions_profile = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_explore = str(0)

            try:
                if impressions_check == "From Hashtags":
                    impressions_hashtags = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div '
                        '> div._75fj > div._759g > div._76la._76l6 > '
                        'div:nth-child(5) > div:nth-child(3) > div > '
                        'div:nth-child(2)')
                    impressions_hashtags = impressions_hashtags.text
            except NoSuchElementException:
                print("Element not found, setting to 0.")
                impressions_hashtags = str(0)

            # Checking what Impression we have in position 5-4-1...
            try:
                impressions_check = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > '
                                                                        'div > div._75fj > div._759g > div._76la._76l6'
                                                                        ' > div:nth-child(5) > div:nth-child(4) > div >'
                                                                        ' div:nth-child(1)').text
            except NoSuchElementException:
                impressions_check = None

            try:
                if impressions_check == "From Profile":
                    impressions_profile = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(4) > div > div:'
                        'nth-child(2)')
                    impressions_profile = impressions_profile.text
                    impressions_explore = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_profile = str(0)

            try:
                if impressions_check == "From Explore":
                    impressions_explore = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div > '
                        'div._75fj > div._759g > div._76la._76l6 > div:'
                        'nth-child(5) > div:nth-child(4) > div > div:'
                        'nth-child(2)')
                    impressions_explore = impressions_explore.text
                    impressions_profile = str(0)
            except NoSuchElementException or impressions_check is None:
                print("Element not found, setting to 0.")
                impressions_explore = str(0)

            try:
                if impressions_check == "From Hashtags":
                    impressions_hashtags = driver.find_element_by_css_selector(
                        '#creator_studio_sliding_tray_root > div > div '
                        '> div._75fj > div._759g > div._76la._76l6 > '
                        'div:nth-child(5) > div:nth-child(4) > div > '
                        'div:nth-child(2)')
                    impressions_hashtags = impressions_hashtags.text
            except NoSuchElementException:
                print("Element not found, setting to 0.")
                impressions_hashtags = str(0)

            try:
                impressions_other = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > '
                                                                        'div > div > div._75fj > div._759g > '
                                                                        'div._76la._76l6 > div:nth-child(5) > '
                                                                        'div:nth-child(5) > div > div:nth-'
                                                                        'child(2)')
                impressions_other = impressions_other.text
            except NoSuchElementException:
                print("Element not found, setting to 0.")
                impressions_other = str(0)

            # Getting the Video from the Post...
            video = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > div > div._75fj > '
                                                        'div._759f > div > div._8oy2 > div._3qn7._61-1._2fyi._3qnf '
                                                        '> video')
            video_url = video.get_attribute("src")

            # Getting Thumbnails from URL...
            insights_images.url_to_img(url=video_url, filename="video_clip" + str(post_num) + ".mp4")

            # Compiling Insight Findings...
            insight_details = {'image url': video_url, 'views': views, 'interactions': interactions,
                               'percentage not following': percentage, 'follows': follows, 'reach': reach,
                               'impressions': impressions, 'from home': impressions_home,
                               'from hashtags': impressions_hashtags, 'from profile': impressions_profile,
                               'from explore': impressions_explore, 'from other': impressions_other}

            # Creating DataFrame
            post_details = pd.DataFrame(insight_details, index=[0])
            details = details.append(post_details, ignore_index=True)

            # Return to Main Post Page
            time.sleep(2)
            go_back = driver.find_element_by_css_selector('#creator_studio_sliding_tray_root > div > '
                                                          'div > div:nth-child(1) > div._6n_t')
            go_back.click()

        # Program Finished...
        if post_num == post_count:
            # Exports all Details to a CSV file at the following path:
            details.to_csv("C://Users/Brianna's HP17/Desktop/overall_details_csv " + mode + ".csv")
