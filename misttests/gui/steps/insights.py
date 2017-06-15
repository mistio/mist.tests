from behave import step


@step(u'the "{section}" section should be visible within {seconds} seconds')
def check_insights_element_visibility(context, section, seconds):
    import ipdb;ipdb.set_trace()
    context.browser.find_element_by_id('machinesList')
    return
