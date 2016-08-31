from behave import step


@step(u'I scroll the clouds list into view')
def scroll_to_top(context):
    context.browser.execute_script("a = document.querySelector('#cloudslist'); if (a != null) { a.scrollIntoView() };")
