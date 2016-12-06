from behave import step

from time import time
from time import sleep

from .machines import comparisons

from .utils import safe_get_element_text

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException


@step(u'I wait for the graphs to appear')
def wait_graphs_to_appear(context):
    try:
        graph_panel = context.browser.find_element_by_tag_name("polyana-dashboard")
        WebDriverWait(graph_panel, 400).until(EC.presence_of_element_located((By.TAG_NAME, "paper-material")))
    except TimeoutException:
        raise TimeoutException("No graphs have appeared after 200 seconds")


@step(u'I focus on the "{graph_title}" graph')
def focus_on_a_graph(context, graph_title):
    try:
        monitoring_area = context.browser.find_element_by_tag_name('polyana-dashboard')
        graph = monitoring_area.find_element_by_xpath("//chart-line[contains(@id, '%s')]" % graph_title)
        position = graph.location['y']
        context.browser.execute_script("window.scrollTo(0, %s)" % position)
    except NoSuchElementException:
            assert False, "Could not find graph with title %s" % graph_title


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
        WebDriverWait(monitoring_area, int(seconds)).until(EC.presence_of_element_located((By.XPATH, "//chart-line[contains(@id, '%s')]" % graph_title)))
    except TimeoutException:
        raise TimeoutException("%s graph has not appeared after %s seconds" % (graph_title, seconds))


def check_graph_tooltip_value(context, graph, operator, wanted_value, tries=3):
    last_point = graph.find_elements_by_tag_name("circle")[-1]
    if last_point:
        hover = ActionChains(context.browser).move_to_element(last_point)
        hover.perform()
        sleep(1)
        try:
            tooltip = graph.find_element_by_css_selector(".c3-tooltip-container")
            tooltip_value = safe_get_element_text(tooltip.find_element_by_css_selector(".value"))
            if tooltip_value:
                if '%' == tooltip_value[-1]:
                    tooltip_value = tooltip_value[:-1]
                if comparisons[operator](int(tooltip_value), wanted_value):
                    return True
        except:
            return False
    else:
        return False

#This works with the new canvas based graphs
@step(u'"{graph_title}" graph should have some values')
def graph_some_value(context, graph_title):
    """
     Checks the graph to see if there is anything drawn
    """
    graph_title = graph_title.lower()
    graph_xpath = '[id^="%s-"]' % graph_title

    try:
        datapoints = context.browser.execute_script("var graph = document.querySelector('%s'); return graph.data.datasets[0].data.length" % graph_xpath)
        if datapoints > 1:
            return
        else:
            assert False, 'Graph does not have any values'
    except NoSuchElementException:
        assert False, "Could not find graph with title %s" % graph_title


#TO REMOVE: This does not work with the new canvas based graphs
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
    monitoring_area = context.browser.find_element_by_tag_name('polyana-dashboard')
    try:
        graph = monitoring_area.find_element_by_xpath("./chart-line[contains(@id, '%s')]" % graph_title)
    except NoSuchElementException:
        assert False, "Could not find graph with title %s" % graph_title

    timeout = time() + int(seconds)
    target_value = float(target_value)
    while time() < timeout:
        try:
            if check_graph_tooltip_value(context, graph, operator, target_value):
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
    graph = context.browser.find_element_by_xpath("//chart-line[contains(@id, '%s')]" % graph_title)

    try:
        parent = graph.find_element_by_xpath("..")
        delete_button = parent.find_element_by_tag_name("paper-icon-button")
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
