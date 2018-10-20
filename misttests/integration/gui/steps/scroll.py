from behave import step


@step(u'I scroll the clouds list into view')
def scroll_to_top(context):
    context.browser.execute_script("window.scrollTo(0,0)")

