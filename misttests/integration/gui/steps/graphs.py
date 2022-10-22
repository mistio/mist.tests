import re
import logging
import requests

from behave import step

from time import time
from time import sleep

from misttests.integration.gui.steps.machines import comparisons

from misttests.integration.gui.steps.utils import safe_get_element_text, get_page_element, expand_shadow_root, scroll_into_view, get_page

from misttests.integration.gui.steps.buttons import clicketi_click
from misttests.integration.gui.steps.forms import get_button_from_form

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

log = logging.getLogger(__name__)


@step('I wait for the monitoring graphs to appear in the "{page}" page')
def wait_graphs_to_appear(context, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    try:
        mist_monitoring = page_shadow.find_element(By.CSS_SELECTOR, 'mist-monitoring')
        container = expand_shadow_root(context, mist_monitoring)
    except NoSuchElementException:
        container = page_shadow
    timeout = time() + 60
    while time() < timeout:
        try:
            polyana_dashboard = container.find_element(By.CSS_SELECTOR, 'polyana-dashboard')
            polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
            WebDriverWait(polyana_dashboard_shadow, 90).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "dashboard-panel")))
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "No graphs have appeared after 150 seconds"


@step('graphs should disappear within {seconds} seconds')
def wait_for_graphs_to_disappear(context, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element(By.CSS_SELECTOR, "polyana-dashboard")
            sleep(1)
        except NoSuchElementException:
            return
    assert False, "Graphs have not disappeared after %s seconds" % seconds


def check_if_graph_is_visible(context, graph_id, timeout, seconds):
    while time() < timeout:
        try:
            context.browser.find_element(By.CSS_SELECTOR, '#' + graph_id)
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "Graph %s has not appeared after %s seconds" % (graph_id, seconds)


@step('{graph_count} graphs should be visible within max {timeout} seconds in the "{page}" page')
def wait_for_all_graphs_to_appear(context, graph_count, timeout, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    try:
        mist_monitoring = page_shadow.find_element(By.CSS_SELECTOR, 'mist-monitoring')
        container = expand_shadow_root(context, mist_monitoring)
    except NoSuchElementException:
        container = page_shadow
    timeout = time() + 30
    while time() < timeout:
        try:
            polyana_dashboard = container.find_element(By.CSS_SELECTOR, 'polyana-dashboard')
            polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
            dashboard_panels = polyana_dashboard_shadow.find_elements(By.CSS_SELECTOR, 'dashboard-panel:not([hidden])')
            if len(dashboard_panels) >= int(graph_count):
                return
        except NoSuchElementException as StaleElementReferenceException:
            sleep(1)
    assert False, "%d graphs appeared after %s seconds" % (len(dashboard_panels), timeout)


@step('I expect the metric buttons to appear within {seconds} seconds')
def wait_metric_buttons(context, seconds):
    from misttests.integration.gui.steps.dialog import get_dialog
    dialog = get_dialog(context, "Select target for graph")
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            expand_shadow_root(context, dialog).find_element(By.CSS_SELECTOR, 'metric-menu')
            return
        except NoSuchElementException as StaleElementReferenceException:
            sleep(1)
    assert False, "Metric buttons inside popup did not appear after %s " \
                  "seconds" % seconds


@step('"{graph_title}" graph should appear in the "{page}" page within {timeout} seconds')
def wait_for_graph_to_appear(context, graph_title, page, timeout):
    return get_graph_panel(context, graph_title, page, timeout)


def get_graph_panel(context, graph_title, page, timeout):
    graph_title = graph_title.lower()
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    try:
        mist_monitoring = page_shadow.find_element(By.CSS_SELECTOR, 'mist-monitoring')
        container = expand_shadow_root(context, mist_monitoring)
    except NoSuchElementException:
        container = page_shadow
    polyana_dashboard = container.find_element(By.CSS_SELECTOR, 'polyana-dashboard')
    polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
    end = time() + int(timeout)
    while time() < end:
        try:
            dashboard_panels = polyana_dashboard_shadow.find_elements(By.CSS_SELECTOR, 'dashboard-panel:not([hidden])')
            for panel in dashboard_panels:
                panel_shadow = expand_shadow_root(context, panel)
                panel_title = safe_get_element_text(panel_shadow.find_element(By.CSS_SELECTOR, 'div.title'))
                if graph_title in panel_title.lower():
                    return panel
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        sleep(2)
    assert False, 'Could not find "%s" graph in %s page within %s seconds' % (graph_title, page, timeout)


@step('"{graph_title}" graph in the "{page}" page should have some values')
def graph_some_value(context, graph_title, page):
    timeout = time() + int(120)
    non_null = []
    while time() < timeout:
        try:
            # Try to get the datapoints for the first available series
            graph_panel = get_graph_panel(context, graph_title, page, 5)
            datapoints = graph_panel.get_property('chartData')['series'][0]['data']
            non_null = [v[1] for v in datapoints if v[1]]
            log.info(graph_panel, len(datapoints), len(non_null))
            if non_null:
                break
        except (IndexError, KeyError):
            sleep(2)
    assert non_null, 'Graph does not have any values'


@step('I give a "{name}" name for my custom metric')
def fill_metric_mame(context, name):
    from misttests.integration.gui.steps.dialog import get_dialog
    dialog = get_dialog(context, "Custom graph")
    dialog_shadow = expand_shadow_root(context, dialog)
    textfield = dialog_shadow.find_element(By.CSS_SELECTOR, "paper-input#name")
    my_metric_name = name
    for letter in my_metric_name:
        textfield.send_keys(letter)


@step('I delete the "{graph_title}" graph in the "{page}" page')
def delete_a_graph(context, graph_title, page):
    graph_title = graph_title.lower()
    graph_panel = get_graph_panel(context, graph_title, page, 5)
    graph_shadow = expand_shadow_root(context, graph_panel)
    try:
        delete_button = graph_shadow.find_element(By.CSS_SELECTOR, "paper-icon-button")
    except NoSuchElementException:
        assert False, "Could not find X button in the graph with title %s" % graph_title
    delete_button.click()
    timeout = time() + 20
    while time() < timeout:
        try:
            graph_panel.is_displayed()
        except Exception:
            return
    assert False, "Graph %s has not disappeared after 20 seconds" % graph_title


@step('I select "{metric}" in the dialog "{dialog}"')
def select_metric_from_dialog(context,metric,dialog):
    if dialog == 'Select target for graph':
        dialog_element = context.browser.find_element(By.CSS_SELECTOR, '#selectTarget')
    else:
        assert False, "Unknown dialog given"
    option_to_click = dialog_element.find_element(By.CSS_SELECTOR, '#' + metric)
    clicketi_click(context,option_to_click)


@step('I click the disable monitoring button for the "{resource_type}"')
def disable_resource_monitoring(context, resource_type):
    page_element = get_page(context, resource_type)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element(By.CSS_SELECTOR, 'mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    menu_button = mist_monitoring_shadow.find_element(By.CSS_SELECTOR, 'paper-menu-button')
    menu_button.click()
    sleep(1)
    menu_button.find_element(By.CSS_SELECTOR, 'paper-button#disable').click()


@step('I select the "{option}" {dropdown} when adding new rule in the "{resource_type}" page')
def select_option_when_adding_rule(context, option, dropdown, resource_type):
    if context.mist_config.get(option):
        option = context.mist_config.get(option)
    page_element = get_page(context, resource_type)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element(By.CSS_SELECTOR, 'mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    new_rule = mist_rules_shadow.find_element(By.CSS_SELECTOR, 'paper-material#add-new-rule-dialog > rule-edit')
    new_rule_shadow = expand_shadow_root(context, new_rule)
    if dropdown in ['team']:
        menu = new_rule_shadow.find_element(By.CSS_SELECTOR, 'mist-dropdown-multi#teams')
        menu_shadow = expand_shadow_root(context, menu)
        menu = menu_shadow.find_element(By.CSS_SELECTOR, 'paper-dropdown-menu')
        selector = 'paper-checkbox:not([hidden])'
    elif dropdown in ['user']:
        menu = new_rule_shadow.find_element(By.CSS_SELECTOR, 'mist-dropdown-multi#members')
        menu_shadow = expand_shadow_root(context, menu)
        menu = menu_shadow.find_element(By.CSS_SELECTOR, 'paper-dropdown-menu')
        selector = 'paper-checkbox:not([hidden])'
    else:
        menu = new_rule_shadow.find_element(By.CSS_SELECTOR, 'paper-dropdown-menu.%s' % dropdown)
        selector = 'paper-item:not([hidden])'
    if menu.find_element(By.CSS_SELECTOR, '.dropdown-content').get_attribute('aria-expanded') != 'true':
        clicketi_click(context, menu)
        sleep(.5)
    item = get_button_from_form(context, menu, option, selector)
    clicketi_click(context, item)
    sleep(.5)
    if menu.find_element(By.CSS_SELECTOR, '.dropdown-content').get_attribute('aria-expanded') == 'true' and dropdown != 'target':
        # If the menu is still open, close it without losing the selected value.
        if 'checkbox' in selector:
            clicketi_click(context, mist_rules_shadow.find_element(By.CSS_SELECTOR, 'paper-material'))
        else:
            clicketi_click(context, item)
        sleep(.5)


@step('I type "{value}" in the {input_class_or_id} when adding new rule in the "{page}" page')
def set_new_rule_threshold(context, value, page, input_class_or_id):
    if context.mist_config.get(value):
        value = context.mist_config.get(value)
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element(By.CSS_SELECTOR, 'mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    new_rule = mist_rules_shadow.find_element(By.CSS_SELECTOR, 'paper-material#add-new-rule-dialog > rule-edit')
    new_rule_shadow = expand_shadow_root(context, new_rule)
    try:
        paper_input = new_rule_shadow.find_element(
            By.CSS_SELECTOR, 'paper-input.%s' % input_class_or_id)
        expand_shadow_root(context, paper_input).find_element(By.CSS_SELECTOR, 'input').send_keys(value)
    except NoSuchElementException:
        try:
            paper_input = new_rule_shadow.find_element(
                By.CSS_SELECTOR, 'paper-textarea.%s' % input_class_or_id)
            paper_input.send_keys(value)
        except NoSuchElementException:
            paper_input = new_rule_shadow.find_element(
                By.CSS_SELECTOR, f'paper-input#{input_class_or_id}'
            )
            expand_shadow_root(context, paper_input).find_element(
                By.CSS_SELECTOR, 'input').send_keys(value)


@step('a new webhook alert should have been posted in slack channel "{channel}" within {seconds} seconds')
def check_slack_webhook(context, channel, seconds):
    if context.mist_config.get(channel):
        channel = context.mist_config.get(channel)

    params={"token": context.mist_config.get('SLACK_WEBHOOK_TOKEN'),
            "channel": channel
    }

    resp = requests.get('https://slack.com/api/conversations.history', params=params)
    assert resp.status_code == 200, "Couldn't connect to Slack api. Response" \
        "status code was %s" % resp.status_code

    current_msgs = resp.json()['messages']

    timeout = time() + int(seconds)
    while time() < timeout:
        resp = requests.get('https://slack.com/api/conversations.history', params=params)
        if resp.json()['messages'] != current_msgs:
            return True
        else:
            sleep(10)
    assert False, "Slack webhook alert has not arrived after %s seconds" % seconds


@step('I save the new rule in the "{page}" page')
def save_new_rule(context, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element(By.CSS_SELECTOR, 'mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    new_rule = mist_rules_shadow.find_element(By.CSS_SELECTOR, 'paper-material#add-new-rule-dialog > rule-edit')
    new_rule_shadow = expand_shadow_root(context, new_rule)
    save_button = get_button_from_form(context, new_rule_shadow, 'save rule')
    clicketi_click(context, save_button)


@step('I remove previous rules in the "{page}" page')
def remove_previous_rules(context, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element(By.CSS_SELECTOR, 'mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    items = mist_rules_shadow.find_elements(By.CSS_SELECTOR, 'rule-item')
    while items:
        item = items.pop()
        item_shadow = expand_shadow_root(context, item)
        try:
            delete_button = item_shadow.find_element(By.CSS_SELECTOR, 'paper-icon-button.delete-btn:not([hidden]):not([disabled])')
            clicketi_click(context, delete_button)
            sleep(1)
            items = mist_rules_shadow.find_elements(By.CSS_SELECTOR, 'rule-item')
        except:
            continue

