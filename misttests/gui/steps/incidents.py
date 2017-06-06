from behave import step
from .utils import safe_get_element_text


@step(u'I should see the incident "{incident}"')
def check_for_incident(context, incident):
    incidents_list = context.browser.find_elements_by_css_selector('div.block div.list')

    for item in incidents_list:
        if incident in safe_get_element_text(item) :
            return

    assert False, "Incident %s was not found in the home page" % incident
