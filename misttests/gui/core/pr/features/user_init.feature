@user-init
Feature: Login Scenarios

  @signup
  Scenario: Sign Up success
    When I make sure user with email "EMAIL" is absent
    Given I am not logged in to mist.core
    When I open the signup popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    Then I follow the link inside the email
    And I delete old emails
    When I enter my standard credentials for signup_password_set
    And I click the go button in the landing page popup
    Then I wait for the dashboard to load
    And I logout
    Given I am not logged in to mist.core
    When I open the signup popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    And I wait for 1 seconds
    Then I should get a conflict error

  @forgot-password
  Scenario: Forgot password
    When I visit mist.core
    When I open the login popup
    And I click the forgot password button in the landing page popup
    And I enter my standard credentials for password_reset_request
    And I click the reset_password_email_submit button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Password reset request" within 10 seconds
    Then I follow the link inside the email
    And I enter my standard credentials for password_reset
    Then I click the reset_pass_submit button in the landing page popup
    And I wait for the dashboard to load
    Then I logout

#  @multiple-login
#  Scenario: Launch two browsers and try to login from both
#    Given I am logged in to mist.core
#    When I launch a second browser
#    And I switch browser
#    When I visit mist.core
#    Given I am logged in to mist.core
#    When I visit the Account page
#    Then I wait for the mist.io splash page to load
#    When I focus on the "Create Token" button
#    And I revoke all sessions
#    Then I wait for 2 seconds
#    When I switch browser
#    And I refresh the page
#    Then I should see the landing page within 10 seconds
#    Then I switch browser
#    When I focus on the "Home" button
#    Then I logout of legacy gui
#    And I quit the second browser
