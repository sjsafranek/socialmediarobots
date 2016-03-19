#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Anthony Lazzaro, and Stefan Safranek"
__copyright__ = "Copyright 2015, Anti-Search Project"
__credits__ = ["Anthony Lazzaro", "Stefan Safranek"]
__license__ = "The MIT License (MIT)"
__version__ = "1.0.1"
__maintainer__ = "Stefan Safranek"
__email__ = "https://github.com/sjsafranek"
__status__ = "Development"

import time
import os
import random
import logging
import builtins
import Conf
import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException


class SeFacebook(object):
    """ Facebook Selenium Interface """
    def __init__(self, username, password, headless=False):
        """ Initiate SeFacebook Class
            Args:
                username (str): Facebook username
                password (str): Facebook password
        """
        FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        LOG_FILENAME = os.path.join("logs","facebook.log")
        logging.basicConfig(
            format=FORMAT, 
            level=logging.DEBUG, 
            # stream=sys.stdout, 
            filename=LOG_FILENAME)
        self.logger = logging.getLogger('Facebook')
        self.logger.info("Username %s", username)
        self.logger.info("Headless %s", headless)
        # setup database
        self.db = Database.DB()
        # Setup driver
        self.username = username
        self.password = password
        if headless:
            self.driver = webdriver.PhantomJS("phantomjs-2.0.0-linux/phantomjs")
        else:
            self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        # options
        self.scrape = True

    def login(self):
        """ Uses username and password to log into Facebook """
        self.driver.get("https://www.facebook.com/")
        username = self.driver.find_element(By.ID,"email")
        username.send_keys(self.username)
        password = self.driver.find_element(By.ID,"pass")
        password.send_keys(self.password)
        login = self.driver.find_element(By.ID,"loginbutton")
        login = login.find_element(By.TAG_NAME,"input")
        login.click()

    def screenshot(self, filename=None):
        """ Saves a screenshot png """
        if not filename:
            filename = str(time.time())
        if '.png' not in filename:
            filename += '.png'
        savefile = os.path.join("SeFacebook", "screenshots", filename + '.png')
        self.driver.save_screenshot(savefile)

    def _slow_type(self,word,elem):
        """ Mimics a human user typing """
        typing_speed = 42 #50 #wpm
        for letter in word:
            elem.send_keys(letter)
            time.sleep(random.random()*10.0/typing_speed)
        elem.send_keys(Keys.ENTER)

    def post(self,text):
        """ Makes a facebook post """
        self.driver.get("https://www.facebook.com/?ref=tn_tnmn")
        pagelet_composer = self.driver.find_element(By.ID,"pagelet_composer")
        forms = pagelet_composer.find_elements(By.TAG_NAME,"form")
        form = forms[1]
        wrap = form.find_element(By.CSS_SELECTOR,"div.wrap")
        innerWrap = wrap.find_element(By.CSS_SELECTOR,"div.innerWrap")
        textarea = innerWrap.find_element(By.CSS_SELECTOR,"textarea")
        self._slow_type(text,textarea)
        buttons = self.driver.find_elements(By.CSS_SELECTOR,"button")
        for button in buttons:
            if "Post" in button.text:
                button.click()
                break

    def set_status(self):
        """ sets a facebook status """
        self.driver.get("https://www.facebook.com/?ref=tn_tnmn")
        pagelet_composer = self.driver.find_element(By.ID,"pagelet_composer")
        forms = pagelet_composer.find_elements(By.TAG_NAME,"form")
        form = forms[1]
        wrap = form.find_element(By.CSS_SELECTOR,"div.wrap")
        innerWrap = wrap.find_element(By.CSS_SELECTOR,"div.innerWrap")
        textarea = innerWrap.find_element(By.CSS_SELECTOR,"textarea")
        options = [
            "Good times","Having fun",
            "Oy vey","Awesome",
            "Totally Tubular","Bitchen",
            "Radical","Groovy",
            "Having a good day",
            "Rock n Roll!" 
        ]
        text = options[random.randint(0,len(options)-1)]
        self._slow_type(text,textarea)
        # LOCATION
        self.driver.find_element(By.ID,"composerCityTagger").click()
        textinputs = self.driver.find_elements(By.CSS_SELECTOR,"input.inputtext.textInput")
        for textinput in textinputs:
            if textinput.get_attribute("aria-label") == "Where are you?":
                textinput.send_keys("Eugene Oregon")
                break
        time.sleep(2)
        places = self.driver.find_element(By.CSS_SELECTOR,"div.PlacesTypeaheadViewList")
        places = places.find_elements(By.CSS_SELECTOR,"li")
        n = random.randint(0,len(places)-1)
        places[n].click()
        # ACTIONS
        time.sleep(2)
        self.driver.find_element(By.ID,"composerActionTagger").click()
        actions = self.driver.find_elements(By.CSS_SELECTOR,"li.action_type")
        n = random.randint(0,len(actions)-1)
        action = actions[n]
        action.click()
        try:
            pages = self.driver.find_elements(By.CSS_SELECTOR,"li.page")
            n = random.randint(0,len(pages)-1)
            page = pages[n]
            page.click()
        except:
            pass
        buttons = self.driver.find_elements(By.CSS_SELECTOR,"button")
        for button in buttons:
            if "Post" in button.text:
                button.click()
                break

    def like_all(self):
        likes = self.driver.find_elements(By.CSS_SELECTOR,"a.UFILikeLink")
        for like in likes:
            if like.text == "Like":
                like.click()

    def close_ads(self):
        section = self.driver.find_element(By.CSS_SELECTOR,"div.ego_unit_container")
        start = time.time()
        while time.time() - start > 60:
            try:
                elements = section.find_elements(By.CSS_SELECTOR, 'a.ego_x.uiCloseButton.uiCloseButtonSmall')
                if len(elements) != 0:
                    section.find_elements(By.CSS_SELECTOR, 'a.ego_x.uiCloseButton.uiCloseButtonSmall')[0].click()
                else:
                    break
                time.sleep(0.75)
            except:
                pass

    def happy_birthdays(self):
        self.driver.get('https://www.facebook.com/events/birthdays')
        div = self.driver.find_element(By.ID,"events_birthday_view")
        text_areas = div.find_elements(By.CSS_SELECTOR,"textarea.enter_submit.uiTextareaNoResize.uiTextareaAutogrow.uiStreamInlineTextarea.inlineReplyTextArea.mentionsTextarea.textInput")
        for textarea in text_areas:
            textarea.send_keys("HAPPY BIRTHDAY!!" + Keys.RETURN)



    def _load_all_friends(self, numTimes=10000):
        """ Cancels loading web page """
        self.logger.info("loading friends...")
        lastNum = 0
        newNum = 1
        num = 0
        while lastNum != newNum and num < numTimes:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.75)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.75)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            lastNum = newNum
            profile_boxes = self.driver.find_elements(By.CLASS_NAME, "uiProfileBlockContent")
            num += 1
            newNum = len(profile_boxes)

    def collectFriends(self):
        self.logger.info("collecting all friends...")
        # Get profile page
        self.logger.debug("getting profile page...")
        links = self.driver.find_elements(By.TAG_NAME, "a")
        links = self.driver.find_elements(By.TAG_NAME, "a")
        for link in links:
            if link.get_attribute("title") == "Profile":
                break
        # Find friends section
        self.driver.get(link.get_attribute("href") + "/friends?source_ref=pb_friends_tl")
        # Load all friends onto page
        self._load_all_friends()
        # get friends
        friends = self.driver.find_elements(By.CLASS_NAME, "uiProfileBlockContent")
        for friend in friends:
            name = friend.text.split("\n")[0]
            firstname = name.split(" ")[0]
            lastname = name.split(" ")[1]
            username = friend.find_elements(By.TAG_NAME,"a")[0].get_attribute("href").split("?")[0].split("/")[-1]
            self.db.createFacebookUser(firstname, lastname, username)

    def logout(self):
        self.driver.get("https://www.facebook.com/?ref=tn_tnmn")
        self.driver.find_element(By.ID,"userNavigationLabel").click()
        for item in self.driver.find_elements(By.CSS_SELECTOR,"li.navSubmenu.__MenuItem"):
            if "Log Out" == item.text:
                item.click()
                break

    def destroy(self):
        try:
            self.logout()
        except:
            pass
        self.driver.quit()

    def __repr__(self):
        return "Facebook %s" % self.username



'''

from selenium.webdriver.common.by import By
from SeFacebook.SeFacebook import SeFacebook
fb = SeFacebook("sjsafranek@gmail.com","sjstmp82")
fb.login()
fb.collectFriends()

'''