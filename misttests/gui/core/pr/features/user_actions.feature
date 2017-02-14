@user-actions
Feature: Login Scenarios and Api Token

  @api-token-test
  Scenario: Create api token and test it with API call
    Given I am logged in to mist.core
    When I visit the Account page
    And I wait for 3 seconds
    Then I click the "API Tokens" button
    #When I revoke all api tokens # needs to be fixed in the backend
    Then I click the "Create API Token" button
    #Create a step that checks if popup with id is open
    #And I expect for "createTokenDialog" popup to appear within max 4 seconds
    And I wait for 2 seconds
    Then I type "Test token" in input with id "tokenName"
    And I wait for 1 seconds
    Then I click the button "Never" from the ttl dropdown
    And I wait for 1 seconds
    Then I type "PASSWORD1" in input with id "pass"
    And I wait for 1 seconds
    And I click the "Create" button
    And I wait for 5 seconds
    When I get the new api token value "BLABLA_TOKEN"
    Then I test the api token "BLABLA_TOKEN". It should work.
    #When i revoke it, it should fail #needs to be fixed in the backend
    #Then I test the api token "BLABLA_TOKEN". It should fail.

  @signup
  Scenario: Sign Up success
    When I make sure user with email "EMAIL" is absent
    Given I am not logged in to mist.core
    When I open the signup popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 30 seconds
    Then I follow the link inside the email
    And I delete old emails
    When I enter my standard credentials for signup_password_set
    And I click the go button in the landing page popup
    Then I wait for the dashboard to load
    And I logout
    Given I am not logged in to mist.core
    When I open the signup popup
    And I wait for 3 seconds
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    And I wait for 3 seconds
    Then I should get a conflict error

  @invalid-credentials
  Scenario: 'Unauthorized' message should appear
    When I visit mist.core
    When I open the login popup
    And I wait for 3 seconds
    And I enter my alt credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 3 seconds
    Then there should be an "Unauthorized" error message inside the "sign in" button

  @invalid-email
  Scenario: Sign in button should not become clickable
    When I wait for 1 seconds
    And I enter my invalid_email credentials for login
    Then the sign in button should be not clickable

  @forgot-password
  Scenario: Forgot password
    When I visit mist.core
    When I open the login popup
    And I wait for 3 seconds
    And I click the forgot password button in the landing page popup
    And I wait for 3 seconds
    And I enter my standard credentials for password_reset_request
    And I click the reset_password_email_submit button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Password reset request" within 30 seconds
    Then I follow the link inside the email
    And I enter my new_creds credentials for password_reset
    Then I click the reset_pass_submit button in the landing page popup
    And I wait for the dashboard to load
    Then I logout
    When I open the login popup
    And I enter my new_creds credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the dashboard to load

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
