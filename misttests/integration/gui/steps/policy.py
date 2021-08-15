from behave import step

from selenium.webdriver.common.keys import Keys

from .forms import get_edit_form

from .buttons import clicketi_click
from .buttons import click_button_from_collection

from .utils import safe_get_element_text, get_page_element, expand_shadow_root
from .utils import clear_input_and_send_keys

from time import sleep


def add_new_rule(context, operator, rtype='all', raction='all', rid='',
                 rtags='', constraints=''):
    operator = operator.lower()
    rtype = rtype.lower()
    raction = raction.lower()
    rid = rid.lower()
    rtags = rtags.lower()

    _, team_page = get_page_element(context, 'teams', 'team')
    team_page_shadow = expand_shadow_root(context, team_page)
    form = team_page_shadow.find_element_by_css_selector('team-policy')
    form_shadow = expand_shadow_root(context, form)
    new_rule = form_shadow.find_element_by_css_selector(
        '#rules > rbac-rule-item:nth-last-child(2)')
    new_rule_shadow = expand_shadow_root(context, new_rule)

    if operator not in ['allow', 'deny']:
        raise Exception('Operator must be either allow or deny')

    if operator == 'allow':
        toggle_button = new_rule_shadow.find_element_by_css_selector('paper-toggle-button')
        clicketi_click(context, toggle_button)

    if rtype != 'all':
        rtype_drop = new_rule_shadow.\
            find_element_by_css_selector('span.resource').\
            find_element_by_css_selector('paper-dropdown-menu')
        clicketi_click(context, rtype_drop)
        sleep(1)
        click_button_from_collection(context, rtype,
                                     rtype_drop.find_elements_by_css_selector('paper-item'))

    if raction != 'all':
        raction_drop = new_rule_shadow.\
            find_element_by_css_selector('span.action').\
            find_element_by_css_selector('paper-dropdown-menu')
        clicketi_click(context, raction_drop)
        sleep(3)
        click_button_from_collection(context, raction,
                                     raction_drop.find_elements_by_css_selector('paper-item'))
    rule_identifier = new_rule_shadow.find_element_by_css_selector('rbac-rule-identifier')
    rule_identifier_shadow = expand_shadow_root(context, rule_identifier)

    rcondition = rule_identifier_shadow.find_element_by_css_selector('paper-dropdown-menu')

    if rid:
        clicketi_click(context, rcondition)
        sleep(1)
        click_button_from_collection(context, 'where id',
                                     rcondition.find_elements_by_css_selector('paper-item'))
        sleep(1)
        rid_drop = rule_identifier_shadow. \
            find_elements_by_css_selector('paper-dropdown-menu')[-1]
        clicketi_click(context, rid_drop)
        sleep(1)
        click_button_from_collection(context, rid,
                                     rid_drop.find_elements_by_css_selector('paper-item'))

    if rtags:
        clicketi_click(context, rcondition)
        sleep(1)
        click_button_from_collection(context, 'where tags',
                                     rcondition.find_elements_by_css_selector('paper-item'))
        sleep(3)
        edit_icon = rule_identifier_shadow. \
            find_element_by_css_selector('.edit')
        clicketi_click(context, edit_icon)
        clicketi_click(context, edit_icon)
        paper_input = rule_identifier_shadow.find_element_by_css_selector('paper-input#inputField')
        paper_input_shadow = expand_shadow_root(context, paper_input)
        input_element = paper_input_shadow.find_element_by_css_selector('input')
        input_element.send_keys(rtags)
    if constraints:            
        constraints_button = new_rule_shadow.find_element_by_css_selector('span.constraints').\
            find_element_by_css_selector('rbac-rule-constraints')
        clicketi_click(context, constraints_button)
        sleep(3)
        overlay = context.browser.find_element_by_css_selector('#overlay')
        overlay_shadow = expand_shadow_root(context, overlay)
        content_div = overlay_shadow.find_element_by_css_selector('#content')
        content_div_shadow = expand_shadow_root(context, content_div)
        mist_form = content_div_shadow.find_element_by_tag_name('mist-form')
        mist_form_shadow = expand_shadow_root(context, mist_form)
        if constraints == "kevin\'s":
            size_constraint_div = mist_form_shadow.find_element_by_id('size_constraint_container')
            size_constraint_toggle = size_constraint_div.find_element_by_tag_name('paper-toggle-button')
            clicketi_click(context, size_constraint_toggle)
            sleep(1)
            primary_disk_constraint_div = size_constraint_div.find_element_by_id('primary_disk_constraint')
            primary_disk_checkbox = primary_disk_constraint_div.find_element_by_tag_name('paper-checkbox')
            clicketi_click(context, primary_disk_checkbox)
            sleep(1)
            swap_disk_constraint_div = size_constraint_div.find_element_by_id('swap_disk_constraint')
            swap_disk_checkbox = swap_disk_constraint_div.find_element_by_tag_name('paper-checkbox')
            clicketi_click(context, swap_disk_checkbox)
            sleep(1)
            field_constraint_div = mist_form_shadow.find_element_by_id('field_constraint_container')
            field_constraint_toggle = field_constraint_div.find_element_by_tag_name('paper-toggle-button')
            clicketi_click(context, field_constraint_toggle)
            sleep(1)
            field_constraint_input = field_constraint_div.find_element_by_css_selector('.mist-form-input')
            field_constraint_shadow = expand_shadow_root(context, field_constraint_input)
            field_constraint_add_button = field_constraint_shadow.find_element_by_tag_name('paper-button')
            clicketi_click(context, field_constraint_add_button)
            sleep(1)
            field_name_paper_input = field_constraint_shadow.find_element_by_tag_name('paper-input')
            field_name_paper_input_shadow = expand_shadow_root(context, field_name_paper_input)
            field_name_iron_input = field_name_paper_input_shadow.find_element_by_tag_name('iron-input')
            field_name_input = field_name_iron_input.find_element_by_tag_name('input')
            field_name_input.send_keys('datastore')
            sleep(1)
        if constraints == "expiration":
            expiration_constraint_div = mist_form_shadow.find_element_by_id('expiration_constraint_container')
            expiration_constraint_toggle = expiration_constraint_div.find_element_by_tag_name('paper-toggle-button')
            clicketi_click(context, expiration_constraint_toggle)
            sleep(1)
            default_duration_field_mist_form = expiration_constraint_div.find_element_by_id('default')
            default_duration_field_mist_form_shadow = expand_shadow_root(context, default_duration_field_mist_form)
            default_duration_paper_input = default_duration_field_mist_form_shadow.find_element_by_tag_name('paper-input')
            default_duration_paper_input_shadow = expand_shadow_root(context, default_duration_paper_input)
            default_duration_iron_input = default_duration_paper_input_shadow.find_element_by_tag_name('iron-input')
            default_duration_input = default_duration_iron_input.find_element_by_tag_name('input')
            default_duration_input.send_keys('12')
            sleep(0.5)
            default_paper_dropdown_menu = default_duration_field_mist_form_shadow.find_element_by_tag_name('paper-dropdown-menu')
            clicketi_click(context, default_paper_dropdown_menu)
            sleep(0.5)
            default_menu_items = default_duration_field_mist_form_shadow.find_elements_by_css_selector('paper-item')
            default_minute_item = None
            for item in default_menu_items:
              if item.get_attribute('value') == 'm':
                  default_minute_item = item
                  break
            clicketi_click(context, default_minute_item)
            sleep(1)
            max_duration_field_mist_form = expiration_constraint_div.find_element_by_id('max')
            max_duration_field_mist_form_shadow = expand_shadow_root(context, max_duration_field_mist_form)
            max_duration_paper_input = max_duration_field_mist_form_shadow.find_element_by_tag_name('paper-input')
            max_duration_paper_input_shadow = expand_shadow_root(context, max_duration_paper_input)
            max_duration_iron_input = max_duration_paper_input_shadow.find_element_by_tag_name('iron-input')
            max_duration_input = max_duration_iron_input.find_element_by_tag_name('input')
            max_duration_input.send_keys('1')
            sleep(0.5)
            max_paper_dropdown_menu = max_duration_field_mist_form_shadow.find_element_by_tag_name('paper-dropdown-menu')
            clicketi_click(context, max_paper_dropdown_menu)
            sleep(0.5)
            max_menu_items = max_duration_field_mist_form_shadow.find_elements_by_css_selector('paper-item')
            max_month_item = None
            for item in max_menu_items:
              if item.get_attribute('value') == 'mo':
                  max_month_item = item
                  break
            clicketi_click(context, max_month_item)
            sleep(1)
            expiration_actions_div = expiration_constraint_div.find_element_by_id('expiration_actions')
            destroy_checkbox = expiration_actions_div.find_element_by_id('destroy')
            clicketi_click(context, destroy_checkbox)
            sleep(0.5)
            expiration_actions_dropdown_menu = expiration_actions_div.find_element_by_tag_name('paper-dropdown-menu')
            clicketi_click(context, expiration_actions_dropdown_menu)
            sleep(0.5)
            destroy_action_item = expiration_actions_div.find_element_by_tag_name('paper-item')
            clicketi_click(context, destroy_action_item)
            sleep(1)
            expiration_notify_div = expiration_constraint_div.find_element_by_id('expiration_notify')
            expiration_notify_subform = expiration_notify_div.find_element_by_tag_name('mist-form-duration-field')
            expiration_notify_subform_shadow = expand_shadow_root(context, expiration_notify_subform)
            expiration_notify_paper_input = expiration_notify_subform_shadow.find_element_by_tag_name('paper-input')
            expiration_notify_paper_input_shadow = expand_shadow_root(context, expiration_notify_paper_input)
            expiration_notify_input = expiration_notify_paper_input_shadow.find_element_by_tag_name('input')
            expiration_notify_input.send_keys(1)
            sleep(0.5)
            expiration_notify_dropdown_menu = expiration_notify_subform_shadow.find_element_by_tag_name('paper-dropdown-menu')
            clicketi_click(context, expiration_notify_dropdown_menu)
            sleep(0.5)
            expiration_notify_minute_item = None
            expiration_notify_dropdown_items = expiration_notify_dropdown_menu.find_elements_by_css_selector('paper-item')
            for item in expiration_notify_dropdown_items:
                if item.get_attribute('value') == 'm':
                    expiration_notify_minute_item = item
            clicketi_click(context, expiration_notify_minute_item)
            sleep(0.5)
            require_checkbox = expiration_notify_div.find_element_by_tag_name('paper-checkbox')
            clicketi_click(context, require_checkbox)
            sleep(1)
        if constraints == "allowed DO VSPHERE":
            vsphere_sizes = [(1024, 1, 15), (2048, 2, 0)]
            # Allow Digital Ocean 2 sizes and VSphere 2 custom sizes
            size_constraint_div = mist_form_shadow.find_element_by_id('size_constraint_container')
            size_constraint_toggle = size_constraint_div.find_element_by_tag_name('paper-toggle-button')
            clicketi_click(context, size_constraint_toggle)
            sleep(1)
            allowed_size_element = size_constraint_div.find_element_by_tag_name('size-element')
            allowed_size_element_shadow = expand_shadow_root(context, allowed_size_element)
            add_allowed_button = allowed_size_element_shadow.find_element_by_tag_name('paper-button')
            for i in range(4):
                clicketi_click(context, add_allowed_button)
                sleep(0.5)
            allowed_dropdowns = allowed_size_element_shadow.find_elements_by_css_selector('paper-dropdown-menu')
            counter=0
            for dropdown in allowed_dropdowns:
                clicketi_click(context, dropdown)
                sleep(0.5)
                cloud_paper_items = dropdown.find_elements_by_css_selector('paper-item')
                if counter < 2:
                    target_cloud = 'DigitalOcean'
                else:
                    target_cloud = 'VMware vSphere'
                for cloud_paper_item in cloud_paper_items:
                    if safe_get_element_text(cloud_paper_item) == target_cloud:
                        clicketi_click(context, cloud_paper_item)
                        sleep(0.5)
                        break
                containing_div = dropdown.find_element_by_xpath('..')
                size_field = containing_div.find_element_by_css_selector('mist-size-field')
                size_field_shadow = expand_shadow_root(context, size_field)
                if counter < 2:
                    size_field_dropdown = size_field_shadow.find_element_by_tag_name('paper-dropdown-menu')
                    clicketi_click(context, size_field_dropdown)
                    sleep(0.5)
                    available_sizes = size_field_dropdown.find_elements_by_css_selector('paper-item')
                    clicketi_click(context, available_sizes[counter])
                    sleep(0.5)
                else:
                    paper_sliders = size_field_shadow.find_elements_by_css_selector('paper-slider')
                    slider_counter = 0
                    for paper_slider in paper_sliders:
                        paper_slider_shadow = expand_shadow_root(context, paper_slider)
                        paper_input = paper_slider_shadow.find_element_by_tag_name('paper-input')
                        paper_input_shadow = expand_shadow_root(context, paper_input)
                        size_input = paper_input_shadow.find_element_by_tag_name('input')
                        size_input.send_keys(Keys.CONTROL + 'a')
                        sleep(0.5)
                        size_input.send_keys(Keys.DELETE)
                        sleep(0.5)
                        # counter is either 2 or 3
                        size_input.send_keys(vsphere_sizes[counter%2][slider_counter])
                        sleep(1)
                        slider_counter += 1
                    # size_name_paper_input = size_field_shadow.find_element_by_tag_name('paper-input')
                    # size_name_paper_input_shadow = expand_shadow_root(context, size_name_paper_input)
                    # human_friendly_input = size_name_paper_input_shadow.find_element_by_tag_name('input')
                    # size_name = 'Vsphere Size {}'.format(counter%2)
                    # human_friendly_input.send_keys(size_name)
                    sleep(1)
                counter += 1

        buttons_div = mist_form_shadow.find_element_by_css_selector('.buttons')
        save_constraints_button = buttons_div.find_element_by_css_selector('.submit-btn')
        clicketi_click(context, save_constraints_button)
        sleep(2)

@step('I add the rule "{operator}" "{rtype}" "{raction}" where id = "{rid}"')
def add_new_rule_with_rid(context, operator, rtype, raction, rid):
    add_new_rule(context, operator, rtype, raction, rid)

@step(u'I add the rule always "{operator}" "{rtype}" "{raction}" with "{constr}" constraints')
def add_new_rule_with_constraints(context, operator, rtype, raction, constr):
    add_new_rule(context, operator, rtype, raction, constraints=constr)

@step('I add the rule "{operator}" "{rtype}" "{raction}" where tags = '
      '"{rtags}"')
def add_new_rule_with_rtags(context, operator, rtype, raction, rtags):
    add_new_rule(context, operator, rtype, raction, rtags=rtags)


@step('I add the rule always "{operator}" "{rtype}" "{raction}"')
def add_new_rule_always(context, operator, rtype, raction):
    add_new_rule(context, operator, rtype, raction)


@step('I remove the rule with index "{index}"')
def delete_rule(context, index):
    _, team_page = get_page_element(context, 'teams', 'team')
    team_page_shadow = expand_shadow_root(context, team_page)
    form = team_page_shadow.find_element_by_css_selector('team-policy')
    form_shadow = expand_shadow_root(context, form)
    rules = [expand_shadow_root(context, rule) for rule in form_shadow.find_elements_by_css_selector('rbac-rule-item')]
    for rule in rules:
        index_class = rule.find_element_by_css_selector('.index')
        rule_index = safe_get_element_text(index_class)
        rule_index = rule_index.replace('.','')
        if rule_index == index:
            delete_btn = rule.find_element_by_css_selector('.delete')
            icon = delete_btn.find_element_by_css_selector('iron-icon')
            clicketi_click(context, icon)
            return
    assert False, "There is no rule with index %s" % index


def check_rule_exists(context, rule_number, operator, rtype, raction, rid, rtags):
    rule_number = int(rule_number)
    operator = operator.lower()
    if operator not in ['allow', 'deny']:
        raise Exception('Operator must be either allow or deny')
    rtype = rtype.lower()
    raction = raction.lower()
    rid = rid.lower()
    rtags = rtags.lower()

    _, team_page = get_page_element(context, 'teams', 'team')
    team_page_shadow = expand_shadow_root(context, team_page)
    form = team_page_shadow.find_element_by_css_selector('team-policy')
    form_shadow = expand_shadow_root(context, form)
    rules = [expand_shadow_root(context, rule) for rule in form_shadow.find_elements_by_css_selector('rbac-rule-item')]
    rule = rules[rule_number]
    rule_operator = safe_get_element_text(
        rule.find_element_by_css_selector('span.operator')).strip().lower()
    assert operator == rule_operator, "Operator is not %s" % operator

    rule_resource = rule.find_element_by_css_selector('span.resource').\
        find_element_by_css_selector('input#input').get_attribute('value').\
        strip().lower()

    assert rtype == rule_resource, "Resource type is not %s" % rtype

    rule_action = rule.find_element_by_css_selector('span.action').\
        find_element_by_css_selector('input#input').get_attribute('value').\
        strip().lower()

    assert raction == rule_action, "Rule action is not %s" % raction

    rcondition = rule.find_element_by_css_selector('span.identifier').\
        find_elements_by_css_selector('input#input')[0].get_attribute('value').\
        strip().lower()

    if not rid and not rtags:
        assert rcondition == 'always', "Rule condition is not always"

    if rid:
        assert rcondition == 'where id', "Rule condition is not always"
        rule_id = rule.find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[1].\
            get_attribute('value').strip().lower()
        assert rid == rule_id, "Rule id is not %s" % rid

    if rtags:
        assert rcondition == 'where tags', "Rule condition is not always"
        rule_tags = rule.find_element_by_css_selector('span.identifier'). \
            find_elements_by_css_selector('input#input')[2].\
            get_attribute('value').strip().lower()
        assert rtags == rule_tags, "Rule tag is not %s" % rtags


@step('rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" where tags'
      ' = "{rtags}"')
def check_rule_with_rtags(context, rule_number, operator, rtype, raction, rtags):
    check_rule_exists(context, rule_number, operator, rtype, raction, '', rtags)


@step('rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" where id = '
      '"{rid}"')
def check_rule_with_rid(context, rule_number, operator, rtype, raction, rid):
    check_rule_exists(context, rule_number, operator, rtype, raction, rid, '')


@step('rule "{rule_number}" is "{operator}" "{rtype}" "{raction}" always')
def check_rule_always(context, rule_number, operator, rtype, raction):
    check_rule_exists(context, rule_number, operator, rtype, raction, '', '')
