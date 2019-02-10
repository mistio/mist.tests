from behave import step

from .buttons import clicketi_click

from .utils import safe_get_element_text, get_page_element, expand_shadow_root


def get_member_list(context):
    _, team_page = get_page_element(context, 'teams', 'team')
    team_shadow = expand_shadow_root(context, team_page)
    return team_shadow.find_element_by_css_selector('paper-material.members')


@step(u'user with email "{email}" should be {user_state}')
def check_user_state(context, email, user_state):
    user_state = user_state.strip().lower()
    if email in context.mist_config:
        email = context.mist_config[email]
    email = email.strip().lower()
    member_list = get_member_list(context)
    members = member_list.find_elements_by_css_selector('paper-item')
    for member in members:
        if email in member.text:
            resend_btn = member.find_element_by_css_selector('#resend')
            if user_state == 'pending' and resend_btn.is_displayed():
                return True
            elif user_state == 'confirmed' and not resend_btn.is_displayed():
                return True
            assert False, "User's(%s) state is not %s" \
                          % (spans[-1], user_state)
    assert False, "User is not among the team members"


@step(u'I delete user "{email}" from team')
def delete_member_from_team(context, email):
    member_list = get_member_list(context)
    members = member_list.find_elements_by_tag_name('paper-item')
    if email in context.mist_config:
        email = context.mist_config[email]
    email = email.strip().lower()
    for member in members:
        if email in member.text:
            button = member.find_element_by_class_name('delete-member')
            clicketi_click(context, button)
            return True
    assert False, "User is not among the team members"
