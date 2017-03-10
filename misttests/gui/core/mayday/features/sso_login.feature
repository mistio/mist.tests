@sso_logins
Feature: Production-sso-testing

  @github_sso_signin
  Scenario: Sign in testing with github
    Given I am not logged in to mist.core
    When I open the login popup
    And I wait for 2 seconds
    Then I click the github button in the landing page popup
    Then I input my "GITHUB_TEST_EMAIL" in the field with id "login_field"
    Then I input my "GITHUB_TEST_PASSWORD" in the field with id "password"
    And I click the Sign In button in the Github form
    And I wait for 3 seconds
    Then I wait for the dashboard to load
    Then I logout

  @google_sso_signin
  Scenario: Sign in testing with google oauth2
    Given I am not logged in to mist.core
    When I open the login popup
    And I wait for 2 seconds
    Then I click the google button in the landing page popup
    Then I input my "GOOGLE_TEST_EMAIL" in the field with id "Email"
    And I click the "next" button
    Then I input my "GOOGLE_TEST_PASSWORD" in the field with id "Passwd"
    And I press the button with id "signIn"
    When I wait for the dashboard to load
    Then I logout
