@user-actions
Feature: Login Scenarios

  @invalid-creds
  Scenario:'Authentication failed' message should appear
    When I visit mist.core
    When I open the login popup
    Then I click the email button in the landing page popup
    # PASSWORD2 needs to be configured, otherwise message is "Enter valid data"
    And I enter my alt credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 1 seconds
    Then there should be a message saying "Authentication failed!" for error in "authentication"
    When I wait for 2 seconds

  @invalid-email
  Scenario: 'Please enter a valid email' message should appear
    When I enter my invalid_email credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 1 seconds
    Then there should be a message saying "Please enter a valid email" for error in "email"
    When I wait for 2 seconds

  @no-password-provided
  Scenario: 'Please enter your password' message should appear
    When I enter my invalid_no_password credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 1 seconds
    Then there should be a message saying "Please enter your password" for error in "password"
    Then I close the "Login" popup
    And I wait for 2 seconds

# test below will probably be deleted...
  @check-redirect
  Scenario: Add Digital Ocean cloud, go to Machines logout and check redirect
    Given I am logged in to mist.core
    And I am in the new UI
    And I wait for 3 seconds
    Given "Digital Ocean" cloud has been added
    Then I logout
    And I visit the machines page with a url
    When I wait for 2 seconds
#    Then I click the email button in the landing page popup
#    When I enter my standard credentials for login
#    And I click the sign in button in the landing page popup
#    Then I wait for the mist.io splash page to load
#    And I should be in the machines page
#    Then I logout
#    And I wait for 2 seconds
