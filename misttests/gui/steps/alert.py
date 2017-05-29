from behave import step


@step(u'I should see the incident "{incident}"')
def check_for_incident(context, incident):
    import ipdb;ipdb.set_trace()
    incidents = context.browser.find_element_by_tag_name('app-incidents')

    return
