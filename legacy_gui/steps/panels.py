from behave import step

from .utils import safe_get_element_text

from .buttons import click_button_from_collection

from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@step(u'I expect for "{panel_id}" panel to {action} within max {seconds} '
      u'seconds')
def panel_waiting_with_timeout(context, panel_id, action, seconds):
    """
    Function that waits for panel to appear but for a maximum amount of time
    """
    if action == 'appear':
        css_selector = '#%s:not([class*="ui-collapsible-collapsed"])' % panel_id
    elif action == 'disappear':
        css_selector = '#%s[class*="ui-collapsible-collapsed"]' % panel_id
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        raise TimeoutException("Panel %s did not %s after %s seconds"
                               % (panel_id, action, seconds))


@step(u'I click the "{text}" button inside the "{panel_title}" panel')
def click_button_within_panel(context, text, panel_title):
    panels = filter(lambda panel: 'ui-collapsible-collapsed' not in
                                  panel.get_attribute('class'),
                    context.browser.find_elements_by_class_name(
                        "ui-collapsible"))
    assert panels, 'No open panels found. Maybe the driver got refocused ' \
                   'or the panel failed to open'

    found_panel = None
    for panel in panels:
        header = panel.find_element_by_class_name("ui-collapsible-heading")
        if panel_title.lower() in safe_get_element_text(header).lower():
            found_panel = panel
            break

    assert found_panel, 'Panel with Title %s could not be found. Maybe the ' \
                        'driver got refocused or the panel failed to open or '\
                        'there is no panel with that title' % panel_title

    buttons = found_panel.find_elements_by_class_name("ui-btn")
    if context.mist_config.get(text):
        text = context.mist_config[text]
    click_button_from_collection(context, text, buttons,
                                 error_message='Could not find %s button'
                                               ' inside %s panel' %
                                               (text, panel_title))


@step(u'I expect for "{side_panel_id}" side panel to {action} within max '
      u'{seconds} seconds')
def side_panel_waiting_with_timeout(context, side_panel_id, action, seconds):
    """
    Function that wait for keyadd-popup to appear but for a maximum
    amount of time
    """
    if action == 'appear':
        css_selector = '#%s[class*="ui-panel-open"]' % side_panel_id
    elif action == 'disappear':
        css_selector = '#%s[class*="ui-panel-closed"]' % side_panel_id
    else:
        raise ValueError("Action can be either appear or disappear. Duh!")
    try:
        WebDriverWait(context.browser, int(seconds)).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
    except TimeoutException:
        raise TimeoutException("Side panel %s did not %s after %s seconds"
                               % (side_panel_id, action, seconds))
