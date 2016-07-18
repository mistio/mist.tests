import json

from behave import *

from time import time
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@step(u'I click the Add provider button')
def click_polymer_button(context):
    import ipdb
    ipdb.set_trace()
    container = context.browser.find_element_by_xpath("//div[contains(@class, 'cloud-add')]")
    button = container.find_element_by_tag_name('paper-button')
    ActionChains(context.browser).move_to_element(button).click().perform()


@step(u'I click the provider button {provider}')
def open_provider_drop_down(context, provider):
    button = context.browser.find_element_by_xpath('//span[contains(text(), "%s")]' %str(provider))
    ActionChains(context.browser).move_to_element(button).click().perform()


@step(u'I expect for "{element_text}" label to be visible within max {seconds} '
      u'seconds')
def element_label_become_visible_waiting_with_timeout(context, element_text, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element_by_xpath('//label[contains(text(), "%s")]' %str(element_text))
            return
        except:
            pass
        assert time() + 1 < timeout, "label %s did not " \
                                     "become visible after %s seconds" % \
                                     (element_text, seconds)
        sleep(1)
