from behave import step

from time import sleep


@step(u'I search for the "{text}" {type_of_search}')
def search_for_something(context, text, type_of_search):
    type_of_search = type_of_search.lower()
    if type_of_search not in ['machine', 'key', 'image', 'script', 'network', 'team']:
        raise ValueError("This is type of object does not exist(%s)" % type_of_search)
    search_bar = context.browser.find_elements_by_class_name("%s-search" % type_of_search)
    assert len(search_bar) > 0, "Could not find the %s-search search input" % type_of_search
    assert len(search_bar) == 1, "Found more than one %s-search search input " \
                                 "elements" % type_of_search
    search_bar = search_bar[0]
    if context.mist_config.get(text):
        text = context.mist_config[text]
    for letter in text:
        search_bar.send_keys(letter)
    sleep(2)
