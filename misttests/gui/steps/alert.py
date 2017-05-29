from behave import step




@step(u'I should see the incident "{incident}"')
def check_for_incident(context, incident):
    from .buttons import clicketi_click

    import ipdb;ipdb.set_trace()
    app_incidents = context.browser.find_element_by_tag_name('app-incidents')
    incidents_list = app_incidents.find_element_by_tag_name('paper-material')
    test = context.browser.find_element_by_css_selector('div.block div.list')
    elem = context.browser.find_elements_by_xpath("//paper-material[contains(@id,'d')]/div")
    # div = incidents_list.find_elements_by_class_name('app-incidents')
    # inner_div = div.find_element_by_tag_name('div')
    # listed_incidents = inner_div.find_elements_by_tag_name('a')
    return
