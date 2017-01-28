@user-actions
Feature: Login Scenarios

  @invalid-creds
  Scenario: 'Unauthorized' message should appear
    When I visit mist.core
    When I open the login popup
    And I enter my alt credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 1 seconds
    Then there should be an "Unauthorized" error message inside the "sign in" button
    When I wait for 2 seconds

  @invalid-email
  Scenario: 'Unauthorized' message should appear
    When I enter my invalid_email credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 1 seconds
    Then there should be an "Unauthorized" error message inside the "sign in" button
    When I wait for 2 seconds

#  @no-password-provided
#  Scenario: 'Please enter your password' message should appear
#    When I enter my invalid_no_password credentials for login
#    And I click the sign in button in the landing page popup
#    And I wait for 1 seconds
#    Then there should be a message saying "Please enter your password" for error in "password"
#    Then I close the "Login" popup
#    And I wait for 2 seconds

 @api-token-test
  Scenario: Create and delete api tokens
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
