@ip-whitelisting
Feature: Ip-whitelisting

# TODO: check what happens when i trigger tests in test_env


  @user-requests-whitelist
  Scenario:  User logs in and requests his ip to be whitelisted. He should receive an email
    When I visit mist.core
    And I wait for 2 seconds
    When I open the login popup
    And I wait for 2 seconds
    And I enter my standard credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 2 seconds
    Then I should see the error message "Trying to login from a non-whitelisted IP address. You can request whitelisting your current IP via email"
    When I click the forbidden link in the sign-in page
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Account IP whitelist request" within 30 seconds


##############################################################
#-- User confirms whitelist
#-- User can now successfully create resources
#-- then "current_ip" should be present
