from behave import step, then

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
    msg = "Log entry is position %s is %s" % (position, time_entry)
    assert time_entry in log_elements[int(position)-1].text, msg
