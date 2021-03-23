@active-directory
Feature: Login scenario

  @AD-login
  Scenario: Log in with Active Directory
    Given "ad" organization and teams are initialized
    Given I am not logged in to mist
    When I visit mist
    And I open the login popup
    And I wait for 3 seconds
    And I click the sign in with active directory button in the landing page popup
    And I enter my ad credentials for ldap login
    And I click the sign in button in the landing page popup
    Then I wait for the navigation menu to appear