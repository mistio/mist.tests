from behave import step

from time import time
from time import sleep

from machines import comparisons

from utils import safe_get_element_text

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


@step(u'I wait for the graphs to appear')
def wait_graphs_to_appear(context):
    try:
        WebDriverWait(context.browser, 400).until(EC.presence_of_element_located((By.CLASS_NAME, "graph")))
    except TimeoutException:
        raise TimeoutException("No graphs have appeared after 200 seconds")


@step(u'I focus on the "{graph_title}" graph')
def focus_on_a_graph(context, graph_title):
    graphs = context.browser.find_elements_by_class_name('graph')
    graph_title = graph_title.lower()
    for graph in graphs:
        if graph_title in safe_get_element_text(graph.find_element_by_class_name('title')).lower():
            position = graph.location['y']
            context.browser.execute_script("window.scrollTo(0, %s)" % position)
            return
    assert False, "Could not find graph with title %s" % graph_title


@step(u'I expect the metric buttons to appear within {seconds} seconds')
def wait_metric_buttons(context, seconds):
    metrics_popup = context.browser.find_element_by_id('metric-add-popup')
    timeout = time() + int(seconds)
    while time() < timeout:
        try:
            metrics_popup.find_element_by_class_name('nest')
            return
        except NoSuchElementException:
            sleep(1)
    assert False, "Metric buttons inside popup did not appear after %s " \
                  "seconds" % seconds


@step(u'"{graph_title}" graph should be added within {seconds} seconds')
def wait_for_graph_to_appear(context, graph_title, seconds):
    timeout = time() + int(seconds)
    graph_title = graph_title.lower()
    while time() < timeout:
        graphs = context.browser.find_elements_by_class_name('graph')
        for graph in graphs:
            graph = graph.find_element_by_class_name('title')
            graph_text = safe_get_element_text(graph)
            if graph_title in graph_text.lower():
                return
        sleep(1)
    assert False, "Graph with title %s has not appeared after %s seconds"\
                  % (graph_title, seconds)


def check_graph_tooltip_value(graph, operator, wanted_value, tries=3):
    graph_rects = graph.find_elements_by_css_selector(".c3-event-rects .c3-event-rect")
    for i in range(1, len(graph_rects)/2):
        rect_selector = ".c3-event-rects .c3-event-rect:nth-last-child(%s)" % i
        try:
            check_point = graph.find_element_by_css_selector(rect_selector)
            check_point.click()
            tooltip = graph.find_element_by_css_selector(".c3-tooltip-container td.value")
            tooltip_text = safe_get_element_text(tooltip)
            tooltip_value = tooltip_text.strip()
            if tooltip_value:
                if '%' == tooltip_value[-1]:
                    tooltip_value = tooltip_value[:-1]
                if comparisons[operator](tooltip_value, wanted_value):
                    return True
        except:
            pass
    return False


@step(u'"{graph_title}" graph should have value {operator} {target_value} '
      u'within {seconds} seconds')
def watch_graph_value(context, graph_title, operator, target_value, seconds):
    """
     Clicks the last point of a cpu graph and takes the value of the tooltip container
     and compare it with zero
    """
    if operator not in comparisons.keys():
        raise ValueError("Operator must be one of these: %s" % comparisons.keys())
    graph_title = graph_title.lower()
    graph_to_watch = None
    graphs = context.browser.find_elements_by_class_name('graph')
    for graph in graphs:
        graph_title_text = safe_get_element_text(graph.find_element_by_class_name('title'))
        if graph_title in graph_title_text.lower():
            graph_to_watch = graph
            break
    assert graph_to_watch, "Graph with title %s has not appeared after %s " \
                           "seconds" % (graph_title, seconds)

    timeout = time() + int(seconds)
    target_value = float(target_value)
    while time() < timeout:
        try:
            if check_graph_tooltip_value(graph_to_watch, operator, target_value):
                return True
        except NoSuchElementException:
            pass
        sleep(1)
    assert False, 'Graph did not get a valid value after %s seconds' % seconds


@step(u'I give a "{name}" name for my custom metric')
def fill_metric_mame(context,name):
    textfield = context.browser.find_element_by_id("custom-plugin-name")
    my_metric_name = name
    for letter in my_metric_name:
        textfield.send_keys(letter)


@step(u'there should be a gap in the "{graph_title}" graph within {seconds}'
      u' seconds')
def check_for_data_gaps(context, graph_title, seconds):
    graph_title = graph_title.lower()
    graph_to_watch = None
    graphs = context.browser.find_elements_by_class_name('graph')
    for graph in graphs:
        if graph_title in safe_get_element_text(graph.find_element_by_class_name('title')).lower():
            graph_to_watch = graph
            break
    assert graph_to_watch, "Could not find graph with title %s" % graph_title
    timeout = time() + int(seconds)
    gap_found = False
    tooltip = graph_to_watch.find_element_by_css_selector(".c3-tooltip-container")
    import ipdb
    ipdb.set_trace()
    while time() < timeout:
        for i in range(1,10):
            check_point = graph_to_watch.find_element_by_css_selector(".c3-event-rects .c3-event-rect:nth-last-child(%s)" % i)
            check_point.click()
            if not tooltip.is_displayed():
                gap_found = True
                break
        if gap_found:
            break
        sleep(10)
    assert gap_found, "No gap in data after %s seconds" % seconds


@step(u'I delete the "{graph_title}" graph')
def delete_a_graph(context, graph_title):
    graph_title = graph_title.lower()
    graph_to_watch = None
    graphs = context.browser.find_elements_by_class_name('graph')
    for graph in graphs:
        if graph_title in safe_get_element_text(graph.find_element_by_class_name('title')).lower():
            graph_to_watch = graph
            break
    assert graph_to_watch, "Could not find graph with title %s" % graph_title
    try:
        x_button = graph_to_watch.find_element_by_class_name('icon-xx')
    except NoSuchElementException:
        assert False, "Could not find X button in the graph with title %s" % graph_title
    x_button.click()
    context.execute_steps(u'''
        Then I expect for "dialog-popup" modal to appear within max 10 seconds
        When I click the "Yes" button inside the "Remove Graph" modal
        Then I expect for "dialog-popup" modal to disappear within max 10 seconds
    ''')
    timeout = time() + 20
    while time() < timeout:
        try:
            graph_to_watch.is_displayed()
        except Exception:
            return
    assert False, "Graph %s has not disappeared after 20 seconds" % graph_title
