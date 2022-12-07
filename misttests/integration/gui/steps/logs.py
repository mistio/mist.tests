from behave import step, then

from time import time
from time import sleep

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.utils import expand_shadow_root, get_page_element


@step('I should see a(n) "{log_type}" log entry of action "{action}" added "{time_entry}" in the "{page}" page within {timeout} seconds')
def check_log_entry_dashboard_page(context, log_type, action, time_entry, page, timeout):
    if page in ['dashboard']:
        mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
        mist_app_shadow = expand_shadow_root(context, mist_app)
        mist_header = mist_app_shadow.find_element(By.CSS_SELECTOR, 'app-header-layout')
        iron_pages = mist_header.find_element(By.CSS_SELECTOR, '#iron-pages')
        pg_dashboard = iron_pages.find_element(By.CSS_SELECTOR, 'page-dashboard')
        pg_dash_shadow = expand_shadow_root(context, pg_dashboard)
        logs = pg_dash_shadow.find_element(By.CSS_SELECTOR, '#logs')
        logs_shadow_root = expand_shadow_root(context, logs)
    else:
        _, container = get_page_element(context, page + 's', page)
        container_shadow = expand_shadow_root(context, container)
        logs_list = container_shadow.find_element(By.CSS_SELECTOR, '#' + page + 'Logs')
        logs_shadow_root  = expand_shadow_root(context, logs_list)

    grid = logs_shadow_root.find_element(By.CSS_SELECTOR, '#grid')
    grid_shadow = expand_shadow_root(context, grid)
    table = grid_shadow.find_element(By.CSS_SELECTOR, '#table')
    items = table.find_element(By.CSS_SELECTOR, '#items')
    _timeout = time() + int(timeout)
    while time() < _timeout:
        log_elements = items.find_elements(By.CSS_SELECTOR, 'tr')
        for log in log_elements:
            if log_type in log.text and action in log.text and time_entry in log.text:
                return

    assert False, "Not found!"
