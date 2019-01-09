from behave import step

from time import time
from time import sleep

from .machines import comparisons

from .utils import safe_get_element_text, get_page_element, expand_shadow_root

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


@step(u'I focus on the "{graph_title}" graph')
def focus_on_a_graph(context, graph_title):
    try:
        monitoring_area = context.browser.find_element_by_tag_name('polyana-dashboard')
        graph = monitoring_area.find_element_by_xpath("//dashboard-panel[contains(., '%s')]" % graph_title)
        position = graph.location['y']
        context.browser.execute_script("window.scrollTo(0, %s)" % position)
    except NoSuchElementException:
            assert False, "Could not find graph with title %s" % graph_title


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
                row_shadow = expand_shadow_root(context, row)
                dashboard_panels += row_shadow.find_elements_by_css_selector('dashboard-panel:not([hidden])')
            if len(dashboard_panels) == int(graph_count):
                return
        except NoSuchElementException:
            sleep(1)
    assert False, "%d graphs appeared after %s seconds" % (len(dashboard_panels), timeout)



@step(u'I expect the metric buttons to appear within {seconds} seconds')
def wait_metric_buttons(context, seconds):
    from .dialog import get_dialog
    dialog = get_dialog(context, "Select target for graph")
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            dialog.find_element_by_css_selector('metric-menu')
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "Metric buttons inside popup did not appear after %s " \
                  "seconds" % seconds


@step(u'"{graph_title}" graph should appear within {seconds} seconds')
def wait_for_graph_to_appear(context, graph_title, seconds):
    graph_title = graph_title.lower()
    monitoring_area = context.browser.find_element_by_tag_name('polyana-dashboard')
    try:
        WebDriverWait(monitoring_area, int(seconds)).until(EC.presence_of_element_located((By.XPATH, "//dashboard-panel[contains(., '%s')]" % graph_title)))
    except TimeoutException:
        raise TimeoutException("%s graph has not appeared after %s seconds" % (graph_title, seconds))


@step(u'"{graph_title}" graph should have some values')
def graph_some_value(context, graph_title):
    #find the right graph
    graph_label = context.browser.find_element_by_xpath('//h3[contains(text(), "%s")]' % graph_title)
    graph_panel = graph_label.find_element_by_xpath('./../..')
    graph_container = graph_panel.find_element_by_id('container')

    #search the page source for the value
    timeout = time() + int(120)
    while time() < timeout:
        #click on the canvas to show the value
        from selenium.webdriver.common import action_chains, keys
        action_chain = ActionChains(context.browser)
        action_chain.move_to_element_with_offset(graph_panel, 600, 150)
        action_chain.click()
        action_chain.perform()
        src = context.browser.page_source
        if graph_title == 'Load on all monitored machines': # graph in dashboard
            machine = context.mist_config['monitored-machine-random']
            text_found = re.search(machine + r" : [0-999]", src)
        else:
            text_found = re.search(graph_title.capitalize() + r" : [0-999]", src)

        if text_found:
            return
        else:
            sleep(2)

    assert False, 'Graph does not have any values'


@step(u'I give a "{name}" name for my custom metric')
def fill_metric_mame(context,name):
    textfield = context.browser.find_element_by_id("custom-plugin-name")
    my_metric_name = name
    for letter in my_metric_name:
        textfield.send_keys(letter)


@step(u'I delete the "{graph_title}" graph')
def delete_a_graph(context, graph_title):
    graph_title = graph_title.lower()
    graph = context.browser.find_element_by_xpath("//dashboard-panel[contains(., '%s')]" % graph_title)

    try:
        delete_button = graph.find_element_by_tag_name("paper-icon-button")
    except NoSuchElementException:
        assert False, "Could not find X button in the graph with title %s" % graph_title
    delete_button.click()

    timeout = time() + 20
    while time() < timeout:
        try:
            graph.is_displayed()
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
