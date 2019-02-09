from behave import step

from time import time
from time import sleep

from .machines import comparisons

from .utils import safe_get_element_text, get_page_element, expand_shadow_root, scroll_into_view, get_page

from .buttons import clicketi_click
from .forms import get_button_from_form

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import re


@step(u'I wait for the monitoring graphs to appear in the "{page}" page')
def wait_graphs_to_appear(context, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element_by_css_selector('mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    timeout = time() + 30
    while time() < timeout:
        try:
            polyana_dashboard = mist_monitoring_shadow.find_element_by_css_selector('polyana-dashboard')
            polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
            WebDriverWait(polyana_dashboard_shadow, 120).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "dashboard-panel")))
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "No graphs have appeared after 150 seconds"


@step(u'graphs should disappear within {seconds} seconds')
def wait_for_graphs_to_disappear(context, seconds):
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            context.browser.find_element_by_tag_name("polyana-dashboard")
            sleep(1)
        except NoSuchElementException:
            return
    assert False, "Graphs have not disappeared after %s seconds" % seconds


def check_if_graph_is_visible(context, graph_id, timeout, seconds):
    while time() < timeout:
        try:
            context.browser.find_element_by_id(graph_id)
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "Graph %s has not appeared after %s seconds" % (graph_id, seconds)


@step(u'{graph_count} graphs should be visible within max {timeout} seconds in the "{page}" page')
def wait_for_all_graphs_to_appear(context, graph_count, timeout, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element_by_css_selector('mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    timeout = time() + 30
    while time() < timeout:
        try:
            polyana_dashboard = mist_monitoring_shadow.find_element_by_css_selector('polyana-dashboard')
            polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
            dashboard_panels = polyana_dashboard_shadow.find_elements_by_css_selector('dashboard-panel:not([hidden])')
            if len(dashboard_panels) >= int(graph_count):
                return
        except NoSuchElementException, StaleElementReferenceException:
            sleep(1)
    assert False, "%d graphs appeared after %s seconds" % (len(dashboard_panels), timeout)


@step(u'I expect the metric buttons to appear within {seconds} seconds')
def wait_metric_buttons(context, seconds):
    from .dialog import get_dialog
    dialog = get_dialog(context, "Select target for graph")
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            expand_shadow_root(context, dialog).find_element_by_css_selector('metric-menu')
            return
        except NoSuchElementException, StaleElementReferenceException:
            sleep(1)
    assert False, "Metric buttons inside popup did not appear after %s " \
                  "seconds" % seconds


@step(u'"{graph_title}" graph should appear in the "{page}" page within {timeout} seconds')
def wait_for_graph_to_appear(context, graph_title, page, timeout):
    return get_graph_panel(context, graph_title, page, timeout)


def get_graph_panel(context, graph_title, page, timeout):
    graph_title = graph_title.lower()
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element_by_css_selector('mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    polyana_dashboard = mist_monitoring_shadow.find_element_by_css_selector('polyana-dashboard')
    polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
    timeout = time() + int(timeout)
    while time() < timeout:
        try:
            dashboard_panels = polyana_dashboard_shadow.find_elements_by_css_selector('dashboard-panel:not([hidden])')
            for panel in dashboard_panels:
                panel_shadow = expand_shadow_root(context, panel)
                panel_title = panel_shadow.find_element_by_css_selector('div.title').text
                if graph_title in panel_title.lower():
                    return panel
        except NoSuchElementException, StaleElementReferenceException:
            pass
        sleep(2)
    assert False, 'Could not find "%s" graph in %s page within %s seconds' % (graph_title, page, timeout)


@step(u'"{graph_title}" graph in the "{page}" page should have some values')
def graph_some_value(context, graph_title, page):
    graph_panel = get_graph_panel(context, graph_title, page, 5)
    timeout = time() + int(120)
    non_null = []
    while time() < timeout:
        try:
            # Try to get the datapoints for the first available series
            datapoints = graph_panel.get_property('chartData')['series'][0]['data']
            non_null = [v[1] for v in datapoints if v[1]]
            if non_null:
                break
        except IndexError, KeyError:
            sleep(2)
    assert non_null, 'Graph does not have any values'


@step(u'I give a "{name}" name for my custom metric')
def fill_metric_mame(context, name):
    from .dialog import get_dialog
    dialog = get_dialog(context, "Custom graph")
    dialog_shadow = expand_shadow_root(context, dialog)
    textfield = dialog_shadow.find_element_by_css_selector("paper-input#name")
    my_metric_name = name
    for letter in my_metric_name:
        textfield.send_keys(letter)


@step(u'I delete the "{graph_title}" graph in the "{page}" page')
def delete_a_graph(context, graph_title, page):
    graph_title = graph_title.lower()
    graph_panel = get_graph_panel(context, graph_title, page, 5)
    graph_shadow = expand_shadow_root(context, graph_panel)
    try:
        delete_button = graph_shadow.find_element_by_css_selector("paper-icon-button")
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


@step(u'I select "{metric}" in the dialog "{dialog}"')
def select_metric_from_dialog(context,metric,dialog):
    if dialog == 'Select target for graph':
        dialog_element = context.browser.find_element_by_id('selectTarget')
    else:
        assert False, "Unknown dialog given"
    option_to_click = dialog_element.find_element_by_id(metric)
    clicketi_click(context,option_to_click)


@step(u'I click the disable monitoring button for the "{resource_type}"')
def disable_resource_monitoring(context, resource_type):
    page_element = get_page(context, resource_type)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element_by_css_selector('mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    menu_button = mist_monitoring_shadow.find_element_by_css_selector('paper-menu-button')
    menu_button.click()
    sleep(1)
    menu_button.find_element_by_css_selector('paper-button#disable').click()


@step(u'I select the "{option}" {dropdown} when adding new rule in the "{resource_type}" page')
def select_option_when_adding_rule(context, option, dropdown, resource_type):
    page_element = get_page(context, resource_type)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element_by_css_selector('mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    new_rule = mist_rules_shadow.find_element_by_css_selector('paper-material#add-new-rule-dialog > rule-edit')
    new_rule_shadow = expand_shadow_root(context, new_rule)
    if dropdown in ['team']:
        menu = new_rule_shadow.find_element_by_css_selector('mist-dropdown-multi#teams')
        menu_shadow = expand_shadow_root(context, menu)
        menu = menu_shadow.find_element_by_css_selector('paper-dropdown-menu')
        selector = 'paper-checkbox:not([hidden])'
    elif dropdown in ['user']:
        menu = new_rule_shadow.find_element_by_css_selector('mist-dropdown-multi#members')
        menu_shadow = expand_shadow_root(context, menu)
        menu = menu_shadow.find_element_by_css_selector('paper-dropdown-menu')
        selector = 'paper-checkbox:not([hidden])'
    else:
        menu = new_rule_shadow.find_element_by_css_selector('paper-dropdown-menu.%s' % dropdown)
        selector = 'paper-item:not([hidden])'
    if menu.find_element_by_css_selector('.dropdown-content').get_attribute('aria-expanded') != 'true':
        clicketi_click(context, menu)
        sleep(.5)
    item = get_button_from_form(context, menu, option, selector)
    clicketi_click(context, item)
    sleep(.5)
    if menu.find_element_by_css_selector('.dropdown-content').get_attribute('aria-expanded') == 'true':
        # If the menu is still open, close it without losing the selected value.
        if 'checkbox' in selector:
            clicketi_click(context, menu)
        else:
            clicketi_click(context, item)
        sleep(.5)


@step(u'I type "{value}" in the {input_class} when adding new rule in the "{page}" page')
def set_new_rule_threshold(context, value, page, input_class):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element_by_css_selector('mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    new_rule = mist_rules_shadow.find_element_by_css_selector('paper-material#add-new-rule-dialog > rule-edit')
    new_rule_shadow = expand_shadow_root(context, new_rule)
    paper_input = new_rule_shadow.find_element_by_css_selector('paper-input.%s' % input_class)
    expand_shadow_root(context, paper_input).find_element_by_css_selector('input').send_keys(value)


@step(u'I save the new rule in the "{page}" page')
def save_new_rule(context, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element_by_css_selector('mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    new_rule = mist_rules_shadow.find_element_by_css_selector('paper-material#add-new-rule-dialog > rule-edit')
    new_rule_shadow = expand_shadow_root(context, new_rule)
    get_button_from_form(context, new_rule_shadow, 'save rule').click()


@step(u'I remove previous rules in the "{page}" page')
def remove_previous_rules(context, page):
    page_element = get_page(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_rules = page_shadow.find_element_by_css_selector('mist-rules')
    mist_rules_shadow = expand_shadow_root(context, mist_rules)
    items = mist_rules_shadow.find_elements_by_css_selector('rule-item')
    while items:
        item = items.pop()
        item_shadow = expand_shadow_root(context, item)
        try:
            delete_button = item_shadow.find_element_by_css_selector('paper-icon-button.delete-btn:not([hidden]):not([disabled])')
            clicketi_click(context, delete_button)
            sleep(1)
            items = mist_rules_shadow.find_elements_by_css_selector('rule-item')
        except:
            continue

