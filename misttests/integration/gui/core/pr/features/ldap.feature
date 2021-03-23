@ldap
Feature: Login scenario

  @LDAP-login
  Scenario: Log in with LDAP
    Given "ldap" organization and teams are initialized
    Given I am not logged in to mist
    When I visit mist
    And I open the login popup
    And I wait for 3 seconds
    And I click the sign in with ldap button in the landing page popup
    And I enter my ldap credentials for ldap login
    And I click the sign in button in the landing page popup
    Then I wait for the navigation menu to appear