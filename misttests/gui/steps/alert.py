from behave import step


@step(u'I should see the incident "{incident}"')
def check_for_incident(context, incident):
    import ipdb;ipdb.set_trace()
    incidents = context.browser.find_element_by_tag_name('app-incidents')
    incidents_list = incidents.find_element_by_tag_name('paper-material')
    listed_incidents = incidents_list.find_elements_by_class_name('list-item')
    return
