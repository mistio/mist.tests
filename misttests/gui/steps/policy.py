from behave import step

from .forms import get_edit_form
from .forms import clear_input_and_send_keys

from .buttons import clicketi_click
from .buttons import click_button_from_collection

from .utils import safe_get_element_text

from time import sleep


def add_new_rule(context, operator, rtype='all', raction='all', rid='',
                 rtags=''):
    operator = operator.lower()
    rtype = rtype.lower()
    raction = raction.lower()
    rid = rid.lower()
    rtags = rtags.lower()

    form = get_edit_form(context, 'policy')
    new_rule_div = form.find_element_by_css_selector(
        '#rules.team-policy > rule-item.team-policy:nth-last-child(2)')

    if operator not in ['allow', 'deny']:
        raise Exception('Operator must be either allow or deny')

    if operator == 'allow':
        toggle_button = new_rule_div.find_element_by_tag_name('paper-toggle-button')
        clicketi_click(context, toggle_button)

    if rtype != 'all':
        rtype_drop = new_rule_div.\
            find_element_by_css_selector('span.resource').\
            find_element_by_css_selector('paper-menu-button#menuButton')
        clicketi_click(context, rtype_drop)
        sleep(1)
        click_button_from_collection(context, rtype,
                                     rtype_drop.find_elements_by_tag_name('paper-item'))

    if raction != 'all':
        raction_drop = new_rule_div.\
            find_element_by_css_selector('span.action').\
            find_element_by_css_selector('paper-menu-button#menuButton')
        clicketi_click(context, raction_drop)
        sleep(4)
        click_button_from_collection(context, raction,
                                     raction_drop.find_elements_by_tag_name('paper-item'))

    rcondition = new_rule_div. \
        find_element_by_css_selector('span.identifier'). \
        find_element_by_css_selector('paper-dropdown-menu')

    if rid:
        clicketi_click(context, rcondition)
        sleep(1)
        click_button_from_collection(context, 'where id',
                                     rcondition.find_elements_by_tag_name('paper-item'))
        sleep(1)
        rid_drop = new_rule_div. \
            find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('paper-dropdown-menu')[-1]
        clicketi_click(context, rid_drop)
        sleep(1)
        click_button_from_collection(context, rid,
                                     rid_drop.find_elements_by_tag_name('paper-item'))

    if rtags:
        clicketi_click(context, rcondition)
        sleep(1)
        click_button_from_collection(context, 'where tags',
                                     rcondition.find_elements_by_tag_name('paper-item'))
        sleep(1)
        input = new_rule_div. \
            find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[-1]
        clear_input_and_send_keys(input, rtags)


@step(u'I add the rule "{operator}" "{rtype}" "{raction}" where id = "{rid}"')
def add_new_rule_with_rid(context, operator, rtype, raction, rid):
    add_new_rule(context, operator, rtype, raction, rid)


@step(u'I add the rule "{operator}" "{rtype}" "{raction}" where tags = '
      u'"{rtags}"')
def add_new_rule_with_rtags(context, operator, rtype, raction, rtags):
    add_new_rule(context, operator, rtype, raction, rtags=rtags)


@step(u'I add the rule always "{operator}" "{rtype}" "{raction}"')
def add_new_rule_always(context, operator, rtype, raction):
    add_new_rule(context, operator, rtype, raction)


def check_rule_exists(context, rule_number, operator, rtype, raction, rid, rtags):
    rule_number = int(rule_number)
    operator = operator.lower()
    rtype = rtype.lower()
    raction = raction.lower()
    rid = rid.lower()
    rtags = rtags.lower()

    form = get_edit_form(context, 'policy')
    rule_div = form.find_element_by_css_selector(
        '#rules.team-policy > div.rule.ruleitem-%s' % rule_number)
    if operator not in ['allow', 'deny']:
        raise Exception('Operator must be either allow or deny')

    rule_operator = safe_get_element_text(
        rule_div.find_element_by_css_selector('span.operator')).strip().lower()

    assert operator == rule_operator, "Operator is not %s" % operator

    rule_resource = rule_div.find_element_by_css_selector('span.resource').\
        find_element_by_css_selector('input#input').get_attribute('value').\
        strip().lower()

    assert rtype == rule_resource, "Resource type is not %s" % rtype

    rule_action = rule_div.find_element_by_css_selector('span.action').\
        find_element_by_css_selector('input#input').get_attribute('value').\
        strip().lower()

    assert raction == rule_action, "Rule action is not %s" % raction

    rcondition = rule_div.find_element_by_css_selector('span.identifier').\
        find_elements_by_css_selector('input#input')[0].get_attribute('value').\
        strip().lower()

    if not rid and not rtags:
        assert rcondition == 'always', "Rule condition is not always"

    if rid:
        assert rcondition == 'where id', "Rule condition is not always"
        rule_id = rule_div.find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[1].\
            get_attribute('value').strip().lower()
        assert rid == rule_id, "Rule id is not %s" % rid

    if rtags:
        assert rcondition == 'where tags', "Rule condition is not always"
        rule_tags = rule_div.find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[2].\
            get_attribute('value').strip().lower()
        assert rtags == rule_tags, "Rule tag is not %s" % rtags


@step(u'rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" where tags'
      u' = "{rtags}"')
def check_rule_with_rtags(context, rule_number, operator, rtype, raction, rtags):
    check_rule_exists(context, rule_number, operator, rtype, raction, '', rtags)


@step(u'rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" where id = '
      u'"{rid}"')
def check_rule_with_rid(context, rule_number, operator, rtype, raction, rid):
    check_rule_exists(context, rule_number, operator, rtype, raction, rid, '')


@step(u'rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" always')
def check_rule_always(context, rule_number, operator, rtype, raction):
    check_rule_exists(context, rule_number, operator, rtype, raction, '', '')
