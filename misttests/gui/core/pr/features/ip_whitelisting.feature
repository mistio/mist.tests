@ip-whitelisting
Feature: Ip-whitelisting

# TODO: check what happens when i trigger tests in test_env

  @whitelist-current-ip
  Scenario:  User whitelists his current IP
    Given I am logged in to mist.core
    When I visit the Account page
    And I wait for 5 seconds
    And I click the "Whitelisted IPs" button with id "ips"
    And I wait for 1 seconds
    And I click the "Add your current ip" button with id "add_current_ip"
    And I wait for 1 seconds
    And I click the "Save IPs" button with id "save_ips"
    Then I expect the dialog "Save IPs" is open within 4 seconds
    When I click the "Save IPs" button in the dialog "Save IPs"
    Then I expect the dialog "Save IPs" is closed within 4 seconds
  # TODO
  # then "current_ip" should be present

  @user-can-create-resources
  Scenario: Verify that user can create resources after whitelisting his own IP
    When I visit the Keys page
    And I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "TestKey" to field "Name" in "key" add form
    And I focus on the button "Generate" in "key" add form
    And I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    Then I expect for the button "Add" in "key" add form to be clickable within 10 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 10 seconds
    When I visit the Keys page
    Then "TestKey" key should be present within 10 seconds

  @set-whitelisted-ips-to-empty
  Scenario:  User sets whitelisted IPs as empty
    When I visit the Account page
    And I wait for 5 seconds
    And I click the "Whitelisted IPs" button with id "ips"
    And I wait for 1 seconds
    And I remove all whitelisted ips
    And I click the "Save IPs" button with id "save_ips"
    Then I expect the dialog "Save IPs" is open within 4 seconds
    # TODO: below 'Save Anyway' is wrong! User won't be locked out
    When I click the "Save Anyway" button in the dialog "Save IPs"
    Then I expect the dialog "Save IPs" is closed within 4 seconds

  @user-can-still-create-resources
  Scenario: Verify that user can still create resources after removing all whitelisted IPs
    When I visit the Keys page
    And I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "TestKey2" to field "Name" in "key" add form
    And I focus on the button "Generate" in "key" add form
    And I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    Then I expect for the button "Add" in "key" add form to be clickable within 10 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 10 seconds
    When I visit the Keys page
    Then "TestKey2" key should be present within 10 seconds

  @save-only-dummy-ip-as-whitelisted
  Scenario:  User sets only a dummy ip as whitelisted. He should be locked out
    When I visit the Account page
    And I wait for 5 seconds
    And I click the "Whitelisted IPs" button with id "ips"
    And I wait for 1 seconds
    And I remove all whitelisted ips
    And I click the button "Add Cidr"
    And I add the IP "1.2.3.4" as whitelisted
    And I click the "Save IPs" button with id "save_ips"
    Then I expect the dialog "Save IPs" is open within 4 seconds
    When I click the "Save Anyway" button in the dialog "Save IPs"
    Then I expect the dialog "Save IPs" is closed within 4 seconds
    And I should see the landing page within 10 seconds

  @user-requests-whitelist
  Scenario:  User logs in and requests his ip to be whitelisted. He should receive an email
    When I visit mist.core
    And I wait for 1 seconds
    And I open the login popup
    And I wait for 1 seconds
    And I enter my standard credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 2 seconds
    Then I should see the error message "Trying to login from a non-whitelisted IP address. You can request whitelisting your current IP via email"
    When I click the forbidden link in the sign-in page
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Account IP whitelist request" within 30 seconds
    When I follow the link inside the email
    And I delete old emails

##############################################################
#-- User can now successfully create resources
#-- then "current_ip" should be present
