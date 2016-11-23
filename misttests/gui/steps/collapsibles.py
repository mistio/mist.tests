from behave import step

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step(u'I expect for "{collapsible_id}" collapsible to {action} within max'
      u' {seconds} seconds')
def panel_waiting_with_timeout(context, collapsible_id, action, seconds):
    """
    Function that waits for collapsible to appear but for a maximum amount of time
    """
    if action == 'appear':
        css_selector = '#%s:not([class*="ui-collapsible-collapsed"])' % collapsible_id
    elif action == 'disappear':
        css_selector = '#%s[class*="ui-collapsible-collapsed"]' % collapsible_id
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        raise TimeoutException("Panel %s did not %s after %s seconds"
                               % (collapsible_id, action, seconds))