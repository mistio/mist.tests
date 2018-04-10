@mayday
Feature: Production

  @add-interval-schedule
  Scenario: Add schedule to be triggered after 5mins
    Given I add the MaydaySchedule via api

  @graph
  Scenario: Production monitor and graph testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the "MAYDAY_MACHINE" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    And "Load" graph should have some values
    When I scroll to the bottom of the page
    And I click the button "Add Graph"
    Then I expect for "selectTarget" modal to appear within max 20 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the popup with id "selectTarget"
    Then "entropy" graph should appear within 30 seconds
    When I focus on the "entropy" graph
    Then "entropy" graph should have some values
    And I delete the "entropy" graph

  @alert
  Scenario: Production rule and alert testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the "MAYDAY_MACHINE" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I remove previous rules
    When I delete old mayday emails
    And I wait for 2 seconds
    And I scroll to the bottom of the page
    And I click the button "add new rule"
    And I wait for 1 seconds
    And I click the "Load" button in the dropdown with id "target-0"
    And I click the "<" button in the dropdown with id "operator-0"
    And I type "10" in input with id "threshold-0"
    And I click the "actionsDropdown" button with id "actionsDropdown"
    And I click the button "alert" in the "actionsDropdown" dropdown
    And I open the "teams" mist-dropdown
    And I select "Owners" in "teams" mist-dropdown
    And I wait for 2 seconds
    And I save the rule

  @celery
  Scenario: Production machine reboot testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the "MAYDAY_MACHINE" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Reboot" from the menu of the "machine" edit form
    Then I expect the dialog "Reboot Machine" is open within 4 seconds
    And I click the "Reboot" button in the dialog "Reboot Machine"
    And I wait for 25 seconds
    Then I click the button "Shell" from the menu of the "machine" edit form
    And I expect terminal to open within 3 seconds
    And I wait for 5 seconds
    And I type in the terminal "uptime"
    And I wait for 1 seconds
    Then up 0 min should be included in the output
    And I close the terminal
    And I wait for 1 seconds

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
    And I click the google button in the landing page popup
    And I input my "GOOGLE_TEST_EMAIL" in the field with id "identifierId"
    And I click the "next" button with id "identifierNext"
    And I wait for 2 seconds
    And I type the password in the Google form
    And I press the button with id "passwordNext"
    Then I wait for the dashboard to load
    And I logout

  @confirm_alert_email
  Scenario: Confirm that alert email arrived
    Then I should receive an email within 200 seconds
    And I wait for 30 seconds

  @incidents
  Scenario: Verify that incident gets triggered
    Given I am logged in to mist.core
    And I wait for the links in homepage to appear
    Then I should see the incident "Load < 10"

  @confirm_schedule-triggered
  Scenario: Verify that schedule got triggered
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    And I search for "mayday-test"
    Then "mayday-test" machine state has to be "stopped" within 300 seconds
