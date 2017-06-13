from behave import step

from time import time
from time import sleep

from .machines import comparisons

from .utils import safe_get_element_text

from .buttons import clicketi_click

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


@step(u'I wait for the graphs to appear')
def wait_graphs_to_appear(context):
    timeout = time() + 20
    while time() < timeout:
        try:
            graph_panel = context.browser.\
                find_element_by_tag_name("polyana-dashboard")
            break
        except NoSuchElementException:
            sleep(1)
    try:
        WebDriverWait(graph_panel, 400).\
            until(EC.presence_of_element_located((By.TAG_NAME, "dashboard-panel")))
    except TimeoutException:
        raise TimeoutException("No graphs have appeared after 200 seconds")


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


@step(u'{graphs} graphs should be visible within max {seconds} seconds')
def wait_for_all_graphs_to_appear(context,graphs,seconds):
    timeout = time() + int(seconds)
    for i in range(0, int(graphs)):
        graph_id = 'panel-' + str(i)
        check_if_graph_is_visible(context,graph_id, timeout, seconds)


@step(u'I expect the metric buttons to appear within {seconds} seconds')
def wait_metric_buttons(context, seconds):
    metrics_popup = context.browser.find_element_by_id('selectTarget')
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            metrics_popup.find_element_by_tag_name('paper-item')
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
    import ipdb;ipdb.set_trace()
    # graph_xpath = '[id^="%s-"]' % graph_title

    graph_xpath = '//*[contains(text(), "%s")]' % graph_title

    # graph_xpath = '//dashboard-panel[contains(text(), "%s")]' % graph_title
    # graph_xpath = "//dashboard-panel[contains(., '%s')]" % graph_title
    try:
        datapoints = context.browser.execute_script("var graph = document.querySelector('%s'); return graph.data.datasets[0].data.length" % graph_xpath)
        # has_datapoints = context.browser.execute_script("var graph = document.querySelector('%s'); return graph.hasRenderedData" % graph_xpath)
        if datapoints:
            return
        else:
            assert False, 'Graph does not have any values'
    except NoSuchElementException:
        assert False, "Could not find graph with title %s" % graph_title


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
