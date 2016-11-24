@user-actions
Feature: Login Scenarios

  @api-token-test
  Scenario: Create and delete api tokens
    Given I am logged in to mist.core
    When I visit the Account page
    Then I wait for the mist.io splash page to load
    When I focus on the "Create Token" button
    And I revoke all api tokens
    Then I click the button "Create Token"
    And I expect for "token-popup-popup" popup to appear within max 4 seconds
    Then I type "blabla" in input with id "new-token-name"
    When I click the button "Create Token"
    And I wait for 1 seconds
    Then I click the button "Never" from the ttl dropdown
    When I click the "Create Token" button inside the "Create Token" popup
    And I wait for 1 seconds
    Then I type "PASSWORD1" in input with id "token-password"
    And I wait for 1 seconds
    When I click the "Submit Password" button inside the "Verify Your Password" popup
    And I wait for 1 seconds
    When I get the new api token value "BLABLA_TOKEN"
    Then I test the api token "BLABLA_TOKEN". It should work.
    When I click the "_x_" button inside the "Token blabla Created" popup
    And I revoke the api token with name blabla
    Then I test the api token "BLABLA_TOKEN". It should fail.
    And I logout
    And I wait for 2 seconds

  @check-error-messages
  Scenario: Make sure that the error messages appear
    When I visit mist.core

    When I open the login popup
    Then I click the email button in the landing page popup
    And I enter my alt credentials for login
    And I click the sign in button in the landing page popup
    Then I expect some reaction within max 3 seconds
    Then there should be a message saying "Authentication failed!" for error in "authentication"
    Then I close the "Login" popup
    And I wait for 1 seconds

    When I open the login popup
    Then I click the email button in the landing page popup
    And I enter my invalid_email credentials for login
    And I click the sign in button in the landing page popup
    Then I expect some reaction within max 3 seconds
    Then there should be a message saying "Please enter a valid email" for error in "email"
    Then I close the "Login" popup
    And I wait for 1 seconds

    When I open the login popup
    Then I click the email button in the landing page popup
    And I enter my invalid_no_password credentials for login
    And I click the sign in button in the landing page popup
    Then I expect some reaction within max 3 seconds
    Then there should be a message saying "Please enter your password" for error in "password"
    Then I close the "Login" popup
    And I wait for 1 seconds

  @check-redirect
  Scenario: Add EC2 cloud, go to Machines logout and check redirect
    Given I am logged in to mist.core
    And I am in the legacy UI
    Given "Linode" cloud has been added
    Then I logout
    And I visit the machines page with a url
    When I wait for 2 seconds
    Then I click the email button in the landing page popup
    When I enter my standard credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the mist.io splash page to load
    And I should be in the machines page
    Then I logout
    And I wait for 2 seconds
