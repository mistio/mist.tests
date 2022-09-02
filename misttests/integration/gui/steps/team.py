from behave import step

from selenium.webdriver.common.by import By

from misttests.integration.gui.steps.buttons import clicketi_click

from misttests.integration.gui.steps.utils import get_page_element
from misttests.integration.gui.steps.utils import expand_shadow_root


def get_member_list(context):
    _, team_page = get_page_element(context, 'teams', 'team')
    team_shadow = expand_shadow_root(context, team_page)
    return team_shadow.find_element(By.CSS_SELECTOR, 'paper-material.members')


@step('user with email "{email}" should be {user_state}')
def check_user_state(context, email, user_state):
    user_state = user_state.strip().lower()
    if email in context.mist_config:
        email = context.mist_config[email]
    email = email.strip().lower()
    member_list = get_member_list(context)
    members = member_list.find_elements(By.CSS_SELECTOR, 'paper-item')
    for member in members:
        if email in member.text:
            resend_btn = member.find_element(By.CSS_SELECTOR, '#resend')
            if user_state == 'pending' and resend_btn.is_displayed():
                return True
            elif user_state == 'confirmed' and not resend_btn.is_displayed():
                return True
            assert False, "User's state is not %s" \
                          % (user_state)
    assert False, "User is not among the team members"


@step('I delete user "{email}" from team')
def delete_member_from_team(context, email):
    member_list = get_member_list(context)
    members = member_list.find_elements(By.CSS_SELECTOR, 'paper-item')
    if email in context.mist_config:
        email = context.mist_config[email]
    email = email.strip().lower()
    for member in members:
        if email in member.text:
            button = member.find_element(By.CSS_SELECTOR, '.delete-member')
            clicketi_click(context, button)
            return True
    assert False, "User is not among the team members"
