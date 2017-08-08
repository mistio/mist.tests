@user-actions
Feature: Login Scenarios and Api Token


  @signup
  Scenario: Sign Up success and verify that user can create resources
    When I make sure user with email "EMAIL" is absent
    Given I am not logged in to mist.core
    When I open the signup popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 30 seconds
    When I follow the link inside the email
    And I delete old emails
    And I enter my standard credentials for signup_password_set
    And I click the go button in the landing page popup
    Then I wait for the links in homepage to appear
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given "Nephoscale" cloud has been added
    And I logout

  @signup-conflict
  Scenario: Already registered user gets conflict error when trying to sign up
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
    When I visit mist.core
    And I open the login popup
    And I wait for 3 seconds
    And I click the forgot password button in the landing page popup
    And I wait for 3 seconds
    And I enter my standard credentials for password_reset_request
    And I click the reset_password_email_submit button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Password reset request" within 30 seconds
    When I follow the link inside the email
    And I enter my new_creds credentials for password_reset
    And I click the reset_pass_submit button in the landing page popup
    And I wait for the links in homepage to appear
    And I logout
    And I open the login popup
    And I enter my new_creds credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the links in homepage to appear
