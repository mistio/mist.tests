@mayday
Feature: Production

  @graph
  Scenario: Production monitor and graph testing
    Given I am logged in to mist.core
    When I wait for the dashboard to load
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I clear the machines search bar
    Then I wait for the graphs to appear
    And I click the button "Add Graph"
    Then I expect for "selectTarget" modal to appear within max 30 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the popup with id "selectTarget"
    And I wait for 6 seconds
    Then "entropy" graph should appear within 30 seconds
    When I focus on the "entropy" graph
    Then "entropy" graph should have some values
    And I delete the "entropy" graph

  @alert
  Scenario: Production rule and alert testing
    Given I am logged in to mist.core
    Then I visit the Home page
    When I wait for the dashboard to load
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I remove previous rules
    When I delete old emails
    And I wait for 2 seconds
    And I focus on the "add new rule" button
    And I click the button "add new rule"
    Then I expect for "newrule" to be visible within max 20 seconds
    And I click the "metricName" rule
    And I click the "RAM" button in the dropdown with id "metricName"
    When I fill "0" as metric value
    And I save the rule
    Then I should receive an email within 200 seconds
    When I remove previous rules

  @ssh
  Scenario: Production ssh testing
    Given I am logged in to mist.core
    Then I visit the Home page
    When I wait for the dashboard to load
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I test the ssh connection 2 times for max 100 seconds each time

  @celery
  Scenario: Production machine reboot testing
    Given I am logged in to mist.core
    Then I visit the Home page
    When I wait for the dashboard to load
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    And I open the actions dialog
    Then I expect for "select-action" modal to appear within max 4 seconds
    When I click the "Reboot" button inside the "select-action" modal
    Then I expect for "confirmation" modal to appear within max 4 seconds
    And I click the button "Reboot"
    Then I expect for "select-action" modal to disappear within max 4 seconds
    And I wait for 4 seconds
    Then Mayday machine state should be "running" within 200 seconds

  @google_sso_signin
  Scenario: Production sign in testing with google oauth2
    Given I am not logged in to mist.core
    When I open the login popup
    Then I click the google button in the landing page popup
    Then I do the Google login
    And I am in the new UI
    When I wait for the dashboard to load
    Then I logout

  @github_sso_signin
  Scenario: Production sign in testing with google oauth2
    Given I am not logged in to mist.core
    When I open the login popup
    Then I click the github button in the landing page popup
    Then I do the Github login
    And I am in the new UI
    When I wait for the dashboard to load
    Then I logout
