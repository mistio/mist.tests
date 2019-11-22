from behave import step, then

from time import time
from time import sleep

from .utils import expand_shadow_root

@step(u'the log entry in position {position} should have been added "{time_entry}"')
def check_log_main_page(context, position, time_entry):
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_tag_name('app-header-layout')
    iron_pages = mist_header.find_element_by_id('iron-pages')
    pg_dashboard = iron_pages.find_element_by_tag_name('page-dashboard')
    pg_dash_shadow = expand_shadow_root(context, pg_dashboard)
    logs = pg_dash_shadow.find_element_by_id('logs')
    logs_shadow = expand_shadow_root(context, logs)
    grid = logs_shadow.find_element_by_id('grid')
    grid_shadow = expand_shadow_root(context, grid)
    table = grid_shadow.find_element_by_id('table')
    items = table.find_element_by_id('items')
    log_elements = items.find_elements_by_tag_name('tr')
    log_el_text = log_elements[int(position)-1].text

    timeout = time() + 5
    while time() < timeout and log_el_text == '':   # log not visible yet
        sleep(1)
        log_elements = items.find_elements_by_tag_name('tr')
        log_el_text = log_elements[int(position)-1].text

    msg = "Log entry in position %s is %s" % (position, log_el_text)
    assert time_entry in log_el_text, msg


@step(u'I should see a(n) "{log_type}" log entry of action "{action}" added "{time_entry}" in the dashboard page within {timeout} seconds')
def check_log_entry_dashboard_page(context, log_type, action, time_entry, timeout):
    mist_app = context.browser.find_element_by_tag_name('mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    mist_header = mist_app_shadow.find_element_by_tag_name('app-header-layout')
    iron_pages = mist_header.find_element_by_id('iron-pages')
    pg_dashboard = iron_pages.find_element_by_tag_name('page-dashboard')
    pg_dash_shadow = expand_shadow_root(context, pg_dashboard)
    logs = pg_dash_shadow.find_element_by_id('logs')
    logs_shadow = expand_shadow_root(context, logs)
    grid = logs_shadow.find_element_by_id('grid')
    grid_shadow = expand_shadow_root(context, grid)
    table = grid_shadow.find_element_by_id('table')
    items = table.find_element_by_id('items')
    _timeout = time() + int(timeout)
    while time() < _timeout:
        log_elements = items.find_elements_by_tag_name('tr')
        for log in log_elements:
            if log_type in log.text and action in log.text and time_entry in log.text:
                return

    assert False, "Not found!"
