#@slow
#Feature: Promos
#
#
#    Background:
#
#        Given promos
#        Given a browser
#        Given a new random mail
#        When I visit mist.io
#            Then I should see "Cloud management in your pocket!"
#
#
#####################################################################################################################################
##              _   __ ____     ____   ____   ____   __  ___ ____  _____
##             / | / // __ \   / __ \ / __ \ / __ \ /  |/  // __ \/ ___/
##            /  |/ // / / /  / /_/ // /_/ // / / // /|_/ // / / /\__ \
##           / /|  // /_/ /  / ____// _, _// /_/ // /  / // /_/ /___/ /
##          /_/ |_/ \____/  /_/    /_/ |_| \____//_/  /_/ \____//____/
##
#####################################################################################################################################
#
#
#    @web
#    Scenario: No promo / Sign Up For Free
#
#            And I wait for 2 seconds
#        When I click the link with text "Sign Up for Free"
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io"
#
#
#    @web
#    Scenario: No promo / Get it / Lite
#
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Lite" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io"
#            Then I should see "You have chosen the "Lite" plan, but in order to give you a taste of our monitoring services, we assigned you a trial."
#            Then I should see "It is completely free and lasts for 15 days, enjoy!"
#            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#    @web
#    Scenario: No promo / Get it / Basic
#
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Basic" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#
#    @web
#    Scenario: No promo / Get it / Startup
#
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Startup" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#
##    @web
##    Scenario: No promo / Get Free Trial
##
##            And I wait for 2 seconds
##        When I click the link with text "Pricing"
##        And I wait for 5 seconds
##            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
##        When I click the link with text "Get Free Trial"
##            Then I should see "Welcome to mist.io!"
##        When I click the link with text "terms of service"
##            Then I should see "PLEASE READ THE FOLLOWING TERMS"
##        When I click outside of the popup
##        And I wait for 5 seconds
##        And I fill in the sign up form
##        And I wait for 2 seconds
##        And I click the "Sign Up" button in "Welcome to mist.io!"
##        And I wait for 5 seconds
##            Then I should receive an email containing "The mist.io bot"
##        When I click the link in the email I received
##            Then I should see "Password set"
##        When I fill in my password
##        And I click the "OK" button
##        And I wait for 4 seconds
##            Then I should see "mist.io"
##            Then I should see "Enjoy your 15-day trial, it's totaly free!"
##            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#####################################################################################################################################
##        ____   ____   ____   __  ___ ____  _____             _   __ ____     ______ __  __ ______ ______ __ __ ____   __  __ ______
##       / __ \ / __ \ / __ \ /  |/  // __ \/ ___/            / | / // __ \   / ____// / / // ____// ____// //_// __ \ / / / //_  __/
##      / /_/ // /_/ // / / // /|_/ // / / /\__ \   ______   /  |/ // / / /  / /    / /_/ // __/  / /    / ,<  / / / // / / /  / /
##     / ____// _, _// /_/ // /  / // /_/ /___/ /  /_____/  / /|  // /_/ /  / /___ / __  // /___ / /___ / /| |/ /_/ // /_/ /  / /
##    /_/    /_/ |_| \____//_/  /_/ \____//____/           /_/ |_/ \____/   \____//_/ /_//_____/ \____//_/ |_|\____/ \____/  /_/
##
#####################################################################################################################################
#
#
#   @web
#    Scenario: Promo / No checkout / Sign Up With Discount
#
#        When I visit a "SINGLE_PLAN_NO_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Sign Up With 20% Off"
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io"
#            Then I should see "In order to give you a taste of our monitoring services, we assigned you a trial."
#            Then I should see "Don't forget that there is a discount waiting just for you on the "account-settings" page. Make sure to use it before it's expiration!"
#            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#    @web
#    Scenario: Promo / No checkout / Get it / Lite
#
#        When I visit a "SINGLE_PLAN_NO_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Lite" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 8 seconds
#            Then I should see "mist.io"
#            Then I should see "You have chosen the "Lite" plan, but in order to give you a taste of our monitoring services, we assigned you a trial."
#            Then I should see "It is completely free and lasts for 15 days, enjoy!"
#            Then I should see "Don't forget that there is a discount waiting just for you on the "account-settings" page. Make sure to use it before it's expiration!"
#            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#    @web
#    Scenario: Promo / No checkout / Get it / Basic / Promo for plan
#
#        When I visit a "SINGLE_PLAN_NO_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Basic" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#
#    @web
#    Scenario: Promo / No checkout / Get it / Startup / Promo not for plan
#
#        When I visit a "SINGLE_PLAN_NO_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Startup" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#
#    @web
#    Scenario: Promo / No checkout / Get it / Startup / Promo for both plans
#
#        When I visit a "DUAL_PLAN_NO_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Startup" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#
##    @web
##    Scenario: Promo / No checkout / Get Free Trial
##
##        When I visit a "SINGLE_PLAN_NO_PURCHASE" promo link
##            And I wait for 2 seconds
##        When I click the link with text "Pricing"
##        And I wait for 5 seconds
##            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
##        When I click the link with text "Get Free Trial"
##            Then I should see "Welcome to mist.io!"
##        When I click the link with text "terms of service"
##            Then I should see "PLEASE READ THE FOLLOWING TERMS"
##        When I click outside of the popup
##        And I wait for 5 seconds
##        And I fill in the sign up form
##        And I wait for 2 seconds
##        And I click the "Sign Up" button in "Welcome to mist.io!"
##        And I wait for 5 seconds
##            Then I should receive an email containing "The mist.io bot"
##        When I click the link in the email I received
##            Then I should see "Password set"
##        When I fill in my password
##        And I click the "OK" button
##        And I wait for 4 seconds
##            Then I should see "mist.io"
##            Then I should see "Enjoy your 15-day trial, it's totaly free!"
##            Then I should see "Don't forget that there is a discount waiting just for you on the "account-settings" page. Make sure to use it before it's expiration!"
##            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#
#####################################################################################################################################
##        ____   ____   ____   __  ___ ____  _____              ______ __  __ ______ ______ __ __ ____   __  __ ______
##       / __ \ / __ \ / __ \ /  |/  // __ \/ ___/             / ____// / / // ____// ____// //_// __ \ / / / //_  __/
##      / /_/ // /_/ // / / // /|_/ // / / /\__ \   ______    / /    / /_/ // __/  / /    / ,<  / / / // / / /  / /
##     / ____// _, _// /_/ // /  / // /_/ /___/ /  /_____/   / /___ / __  // /___ / /___ / /| |/ /_/ // /_/ /  / /
##    /_/    /_/ |_| \____//_/  /_/ \____//____/             \____//_/ /_//_____/ \____//_/ |_|\____/ \____/  /_/
##
#####################################################################################################################################
#
#
#
#    @web
#    Scenario: Single Plan Promo / Checkout / Sign Up With Discount
#
#        When I visit a "SINGLE_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Sign Up With 20% Off"
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 6 seconds
#            Then I should not see "Loading"
#
#
#    @web
#    Scenario: Single Plan Promo / Checkout / Get it / Lite
#
#        When I visit a "SINGLE_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Lite" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io"
#            Then I should see "You have chosen the "Lite" plan, but in order to give you a taste of our monitoring services, we assigned you a trial."
#            Then I should see "It is completely free and lasts for 15 days, enjoy!"
#            Then I should see "Don't forget that there is a discount waiting just for you on the "account-settings" page. Make sure to use it before it's expiration!"
#            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#    @web
#    Scenario: Single Plan Promo / Checkout / Get it / Basic / Promo for plan
#
#        When I visit a "SINGLE_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Basic" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 6 seconds
#            Then I should not see "Loading"
#
#
#    @web
#    Scenario: Single Plan Promo / Checkout / Get it / Startup / Promo not for plan
#
#        When I visit a "SINGLE_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Startup" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 6 seconds
#            Then I should not see "Loading"
#
#    @web
#    Scenario: Dual Plan Promo / Checkout / Get it / Basic
#
#        When I visit a "DUAL_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Basic" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#
#    @web
#    Scenario: Dual Plan Promo / Checkout / Get it / Startup
#
#        When I visit a "DUAL_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Pricing"
#        And I wait for 5 seconds
#            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
#        When I click the "Startup" get it button
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 4 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "Loading"
#        When I wait for 5 seconds
#            Then I should not see "Loading"
#
#    @web
#    Scenario: Dual Plan Promo / Checkout /  Sign Up With Discount
#
#        When I visit a "DUAL_PLAN_PURCHASE" promo link
#            And I wait for 2 seconds
#        When I click the link with text "Sign Up With 20% Off"
#        And I wait for 5 seconds
#            Then I should see "Welcome to mist.io!"
#        When I click the link with text "terms of service"
#            Then I should see "PLEASE READ THE FOLLOWING TERMS"
#        When I click outside of the popup
#        And I wait for 5 seconds
#        And I fill in the sign up form
#        And I wait for 2 seconds
#        And I click the "Sign Up" button in "Welcome to mist.io!"
#        And I wait for 5 seconds
#            Then I should see "Thanks for signing up!" within 60 seconds
#            Then I should receive an email containing "The mist.io bot"
#        When I click the link in the email I received
#            Then I should see "Password set"
#        When I fill in my password
#        And I click the "OK" button
#        And I wait for 6 seconds
#            Then I should see "mist.io - account settings"
#            Then I should see "There is a discount waiting just for you. Go ahead and pick the offer that suits you best!"
#            Then I should see "When done, click the "Home" button."
#
#
##    @web
##    Scenario: Single Plan Promo / Checkout / Get Free Trial
##
##        When I visit a "SINGLE_PLAN_PURCHASE" promo link
##            And I wait for 2 seconds
##        When I click the link with text "Pricing"
##        And I wait for 5 seconds
##            Then I should see "Pricing"
##            Then I should see "Not sure yet ?"
##        When I click the link with text "Get Free Trial"
##            Then I should see "Welcome to mist.io!"
##        When I click the link with text "terms of service"
##            Then I should see "PLEASE READ THE FOLLOWING TERMS"
##        When I click outside of the popup
##        And I wait for 5 seconds
##        And I fill in the sign up form
##        And I wait for 2 seconds
##        And I click the "Sign Up" button in "Welcome to mist.io!"
##        And I wait for 5 seconds
##            Then I should receive an email containing "The mist.io bot"
##        When I click the link in the email I received
##            Then I should see "Password set"
##        When I fill in my password
##        And I click the "OK" button
##        And I wait for 4 seconds
##            Then I should see "mist.io"
##            Then I should see "Enjoy your 15-day trial, it's totaly free!"
##            Then I should see "Don't forget that there is a discount waiting just for you on the "account-settings" page. Make sure to use it before it's expiration!"
##            Then I should see "To manage your account settings click "Me" > "My account"."
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#