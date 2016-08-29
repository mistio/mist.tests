from tests.legacy_gui.steps.promos import *
# """  File : promos.py
#
#    When:
#        I fill in a random password                                 |login_fillin_random_password()
#
#    Then:
#        I should receive an email containing "{text}"               |login_receive_email_containing_text()
#
#
# """
# from time import sleep
# from random import randrange, random
# from behave import given, when, then
#
# from login import MIST_URL
#
# from mist.core import config
#
# #PROMOS
# promos = {}
# #SINGLE_PLAN_NO_PURCHASE = ''
# #SINGLE_PLAN_PURCHASE = ''
# #DUAL_PLAN_NO_PURCHASE = ''
# #DUAL_PLAN_PURCHASE = ''
#
#
# @given(u'promos')
# def clouds_credentials(context):
#     import os
#
#     global promos
#
#     promos = config.PROMO_CODES
#
#     #SINGLE_PLAN_NO_PURCHASE = promos['SINGLE_PLAN_NO_PURCHASE']
#     #SINGLE_PLAN_PURCHASE = promos['SINGLE_PLAN_PURCHASE']
#     #DUAL_PLAN_NO_PURCHASE = promos['DUAL_PLAN_NO_PURCHASE']
#     #DUAL_PLAN_PURCHASE = promos['DUAL_PLAN_PURCHASE']
#
#
# @given(u'a new random mail')
# def given_new_random_mail(context):
#     i = int(random()*10000000)
#     context.email = "test%d@mist.io" % i
#
#
# @when(u'I visit a "{promo_type}" promo link')
# def visit_promo_link(context, promo_type):
#     context.browser.visit(MIST_URL + '/?p=' + promos[str(promo_type)])
#
#
# @when(u'I click the "{plan_text}" get it button')
# def click_get_it_button_by_plan_text(context, plan_text):
#     index = -1
#     if plan_text == 'Lite': index = 0
#     if plan_text == 'Basic': index = 1
#     if plan_text == 'Startup': index = 2
#     context.browser.find_by_css('.price-grid a')[index].click()
