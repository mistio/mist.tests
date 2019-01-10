from behave import step

from time import time
from time import sleep

from .machines import comparisons

from .utils import safe_get_element_text, get_page_element, expand_shadow_root, scroll_into_view

from .buttons import clicketi_click

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

import re


@step(u'I wait for the monitoring graphs to appear in the "{page}" page')
def wait_graphs_to_appear(context, page):
    if page in ['machine']:
        _, page_element = get_page_element(context, page + 's', page)
    else:
        page_element = get_page_element(context, page)
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
                    (By.CSS_SELECTOR, "dashboard-row")))
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
    if page in ['machine']:
        _, page_element = get_page_element(context, page + 's', page)
    else:
        page_element = get_page_element(context, page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element_by_css_selector('mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    timeout = time() + 30
    while time() < timeout:
        try:
            dashboard_panels = []
            polyana_dashboard = mist_monitoring_shadow.find_element_by_css_selector('polyana-dashboard')
            polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
            dashboard_rows = polyana_dashboard_shadow.find_elements_by_css_selector('dashboard-row:not([hidden])')
            for row in dashboard_rows:
                scroll_into_view(context, row)
                row_shadow = expand_shadow_root(context, row)
                dashboard_panels += row_shadow.find_elements_by_css_selector('dashboard-panel:not([hidden])')
            if len(dashboard_panels) == int(graph_count):
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
        except NoSuchElementException:
            sleep(1)
    assert False, "Metric buttons inside popup did not appear after %s " \
                  "seconds" % seconds


@step(u'"{graph_title}" graph should appear in the "{page}" page within {timeout} seconds')
def wait_for_graph_to_appear(context, graph_title, page, timeout):
    return get_graph_panel(context, graph_title, page, timeout)

def get_graph_panel(context, graph_title, page, timeout):
    graph_title = graph_title.lower()
    if page == 'dashboard':
        page_element = get_page_element(context, 'dashboard')
    else:
        _, page_element = get_page_element(context, page + 's', page)
    page_shadow = expand_shadow_root(context, page_element)
    mist_monitoring = page_shadow.find_element_by_css_selector('mist-monitoring')
    mist_monitoring_shadow = expand_shadow_root(context, mist_monitoring)
    polyana_dashboard = mist_monitoring_shadow.find_element_by_css_selector('polyana-dashboard')
    polyana_dashboard_shadow = expand_shadow_root(context, polyana_dashboard)
    timeout = time() + int(timeout)
    while time() < timeout:
        dashboard_rows = polyana_dashboard_shadow.find_elements_by_css_selector('dashboard-row:not([hidden])')
        dashboard_panels = []
        for row in dashboard_rows:
            row_shadow = expand_shadow_root(context, row)
            dashboard_panels += row_shadow.find_elements_by_css_selector('dashboard-panel:not([hidden])')
        for panel in dashboard_panels:
            panel_shadow = expand_shadow_root(context, panel)
            panel_title = panel_shadow.find_element_by_css_selector('h3').text
            if graph_title in panel_title.lower():
                return panel
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
