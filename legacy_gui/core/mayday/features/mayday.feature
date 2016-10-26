@mayday
Feature: Production

  @graph
  Scenario: Production monitor and graph testing
    Given I am logged in to mist.core
    Then I wait for the links in homepage to appear
    When I visit the Machines page after the counter has loaded
    Then I search for the "Mayday" Machine
    When I click the button "Mayday"
    Then I expect for "single-machine-page" page to appear within max 10 seconds
    Then I wait for the graphs to appear
    When I focus on the "Add Graph" button
    And I click the button "Add Graph"
    Then I expect for "metric-add-popup" popup to appear within max 30 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the "Select Metric" popup
    Then "entropy" graph should be added within 30 seconds
    When I focus on the "entropy" graph
    Then "entropy" graph should have value > 0 within 30 seconds
    And I delete the "entropy" graph

  @alert
  Scenario: Production rule and alert testing
    Given I am logged in to mist.core
    Then I wait for the links in homepage to appear
    When I visit the Machines page after the counter has loaded
    Then I search for the "Mayday" Machine
    When I click the button "Mayday"
    Then I expect for "single-machine-page" page to appear within max 10 seconds
    Then I wait for the graphs to appear
    When I remove previous rules
    When I delete old emails
    When I focus on the "Add Rule" button
    And I click the button "Add Rule"
    Then I expect for "basic-condition" to be visible within max 20 seconds
    And I expect for buttons inside "basic-condition" to be clickable within max 20 seconds
    And I click the button "Load"
    And I click the button "RAM"
    When I fill "0" as rule value
    Then I should receive an email within 300 seconds
    When I remove previous rules

  @ssh
  Scenario: Production ssh testing
    Given I am logged in to mist.core
    Then I wait for the links in homepage to appear
    When I visit the Machines page after the counter has loaded
    Then I search for the "Mayday" Machine
    When I click the button "Mayday"
    Then I expect for "single-machine-page" page to appear within max 10 seconds
    Then I wait for the graphs to appear
    When I test the ssh connection 2 times for max 100 seconds each time

  @celery
  Scenario: Production machine reboot testing
    Given I am logged in to mist.core
    Then I wait for the links in homepage to appear
    When I visit the Machines page after the counter has loaded
    Then I search for the "Mayday" Machine
    When I choose the "Mayday" machine
    And I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the "Reboot" button inside the "Actions" popup
    Then I expect for "dialog-popup" modal to appear within max 4 seconds
    And I click the button "Yes"
    Then I expect for "dialog-popup" modal to disappear within max 4 seconds
    And I wait for 4 seconds
    Then "Mayday" machine state should be "running" within 200 seconds

  @google_sso_signin
  Scenario: Production sign in testing with google oauth2
    Given I am not logged in to mist.core
    When I open the login popup
    Then I click the google button in the landing page popup
    Then I do the Google login
    And I wait for the links in homepage to appear
    Then I logout

  @github_sso_signin
  Scenario: Production sign in testing with google oauth2
    Given I am not logged in to mist.core
    When I open the login popup
    Then I click the github button in the landing page popup
    Then I do the Github login
    And I wait for the links in homepage to appear
    Then I logout
