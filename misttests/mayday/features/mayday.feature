@mayday
Feature: Production

  @add-interval-schedule
  Scenario: Add schedule to be triggered after 5mins
    Given I add the MaydaySchedule via api

  @graph
  Scenario: Production monitor and graph testing
    Given I am logged in to mist
    When I visit the Machines page after the counter has loaded
    Then I search for "MAYDAY_MACHINE"
    And I wait for 1 seconds
    When I click the "MAYDAY_MACHINE" "machine"
    And I clear the search bar
    And I expect the "machine" page to be visible within max 5 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
#    And "Load" graph should have some values
#    When I scroll to the bottom of the page
#    And I click the button "Add Graph"
#    Then I expect for "selectTarget" modal to appear within max 20 seconds
#    And I expect the metric buttons to appear within 30 seconds
#    When I click the "entropy" button inside the popup with id "selectTarget"
#    Then "entropy" graph should appear within 30 seconds
#    Then "entropy" graph should have some values
#    And I delete the "entropy" graph

  @alert
  Scenario: Production rule and alert testing
    Given I am logged in to mist
    When I visit the Machines page after the counter has loaded
    Then I search for "MAYDAY_MACHINE"
    And I wait for 1 seconds
    When I click the "MAYDAY_MACHINE" "machine"
    And I clear the search bar
    And I expect the "machine" page to be visible within max 5 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
    When I scroll to the rules section in the "machine" page
    When I remove previous rules in the "machine" page
    When I delete old mayday emails
    And I wait for 2 seconds
    And I I scroll to the rules section in the "machine" page
    And I click the button "add new rule" in the "machine" page
    And I wait for 1 seconds
    And I select the "Load" target when adding new rule in the "machine" page
    And I select the "<" operator when adding new rule in the "machine" page
    And I type "10" in the threshold when adding new rule in the "machine" page
    And I select the "alert" action when adding new rule in the "machine" page
    And I select the "Owners" team when adding new rule in the "machine" page
    And I wait for 2 seconds
    And I save the new rule in the "machine" page

  @reboot
  Scenario: Production machine reboot testing
    Given I am logged in to mist
    When I visit the Machines page after the counter has loaded
    And I clear the search bar
    And I wait for 1 seconds
    Then I search for "MAYDAY_MACHINE"
    When I click the "MAYDAY_MACHINE" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Reboot" action button in the "machine" page
    Then I expect the "Reboot Machine" dialog to be open within 4 seconds
    When I click the "Reboot" button in the "Reboot Machine" dialog
    And I wait for 40 seconds
    Then I click the "Shell" action button in the "machine" page
    And I expect terminal to open within 3 seconds
    And I wait for 5 seconds
    And I type in the terminal "uptime"
    And I wait for 1 seconds
    Then up 0 min should be included in the output
    And I close the terminal
    And I wait for 1 seconds
    And I logout

  @github_sso_signin
  Scenario: Sign in testing with github
    Given I am not logged in to mist
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
    Given I am not logged in to mist
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
    Given I am logged in to mist
    And I wait for the navigation menu to appear
    And I wait for 2 seconds
    Then I should see the incident "Load < 10"

  @confirm_schedule-triggered
  Scenario: Verify that schedule got triggered
    Given I am logged in to mist
    When I visit the Machines page after the counter has loaded
    And I search for "mayday-test"
    Then "mayday-test" machine state has to be "stopped" within 300 seconds

  @celery
  Scenario: Verify that list_machines has run within the last 90 seconds
    Given I verify that machine with id "MAYDAY_MACHINE_ID" has been seen the last 90 seconds
