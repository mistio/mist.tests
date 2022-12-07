@user-actions
Feature: Login Scenarios and Api Token

  @api-token-test
  Scenario: Create api token and test it with API call. When it is revoked, API call should fail
    Given I am logged in to mist
    When I visit the Account page
    And I wait for 2 seconds
    And I click the "API Tokens" tab in the Account page
    And I click the "Create API Token" button in the Account page
    Then I expect the "Create API Token" dialog to be open within 4 seconds
    And I set the value "Test token" to field "Token Name" in the "Create API Token" dialog
    And I wait for 1 seconds
    And I open the "Expires After" dropdown in the "Create API Token" dialog
    And I click the "Never" button in the "Expires After" dropdown in the "Create API Token" dialog
    And I wait for 1 seconds
    And I click the "Create" button in the "Create API Token" dialog
    And I wait for 3 seconds
    And I get the new api token value "BLABLA_TOKEN"
    Then I test the api token "BLABLA_TOKEN". It should work.
    When I revoke token "Test token"
    And I wait for 1 seconds
    Then I test the api token "BLABLA_TOKEN". It should fail.

  @signup
  Scenario: Sign Up success and verify that user can create resources
    When I make sure user with email "EMAIL" is absent
    Given I am not logged in to mist
    When I visit the signup page
    And I wait for 2 seconds
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "Confirm your registration" within 30 seconds
    When I follow the link inside the email
    And I delete old emails
    And I wait for 2 seconds
    And I enter my standard credentials for signup_password_set
    And I click the go button in the landing page popup
    Then I wait for the navigation menu to appear
    When I visit the Home page
    And I save the org name if necessary
    Given "Linode" cloud has been added

  @change-password
  Scenario: Change password from Account page and verify it worked
#    When I visit the Account page
#    And I wait for 3 seconds
#    And I click the "Password" button with id "Password"
#    And I wait for 2 seconds
#    Then I type "PASSWORD1" in input with id "currentPassword"
#    Then I type "CHANGED_PASSWORD" in input with id "newPassword"
#    Then I type "CHANGED_PASSWORD" in input with id "confirmNewPassword"
#    And I click the button "Change Password"
#    And I wait for 2 seconds
#    And I logout
#    When I visit mist
#    And I open the login popup
#    And I wait for 3 seconds
#    And I enter my changed credentials for login
#    And I click the sign in button in the landing page popup
#    And I wait for 3 seconds
#    Then I wait for the navigation menu to appear
    And I logout

  @signup-conflict
  Scenario: Already registered user gets conflict error when trying to sign up
    Given I am not logged in to mist
    When I visit the signup page
    And I wait for 2 seconds
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    And I wait for 3 seconds
    Then I should get a conflict error

  @invalid-credentials
  Scenario: 'Unauthorized' message should appear
    When I visit mist
    And I open the login popup
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
    When I visit mist
    And I open the login popup
    And I wait for 3 seconds
    And I click the forgot password button in the landing page popup
    And I wait for 3 seconds
    And I enter my standard credentials for password_reset_request
    And I click the reset_password_email_submit button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "Password reset request" within 30 seconds
    When I follow the link inside the email
    And I wait for 2 seconds
    And I enter my new_creds credentials for password_reset
    And I click the reset_pass_submit button in the landing page popup
    And I wait for the navigation menu to appear
    And I logout
    And I open the login popup
    And I enter my new_creds credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the navigation menu to appear
