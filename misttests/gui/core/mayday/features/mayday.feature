@mayday
Feature: Production

  @graph
  Scenario: Production monitor and graph testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
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
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I remove previous rules
    When I delete old mayday emails
    And I wait for 2 seconds
    And I focus on the "add new rule" button
    And I click the button "add new rule"
    Then I expect for "newrule" to be visible within max 20 seconds
    And I click the "metricName" rule
#    And I click the "RAM" button in the dropdown with id "metricName"
    When I fill "0" as metric value
    And I save the rule
#    When I remove previous rules

  @ssh
  Scenario: Production ssh testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I test the ssh connection 2 times for max 100 seconds each time

  @celery
  Scenario: Production machine provisioning testing
    Given I am logged in to mist.core
    And I wait for the dashboard to load
    Given "AWS" cloud has been added
    When I refresh the page
    And I wait for the dashboard to load
    And I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    And I click the button "AWS" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "AWS" to create the "docker-mayday-test-machine-random" machine
    And I select the mayday key
    And I wait for 3 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I wait for 2 seconds
    And I click the "Launch" button with id "appformsubmit"
    And I wait for 5 seconds
    Then "docker-mayday-test-machine-random" machine state has to be "running" within 300 seconds
    Then I search for the machine "docker-mayday-test-machine-random"
    When I click the "docker-mayday-test-machine-random" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Destroy" from the menu of the "machine" edit form
    And I expect the dialog "Destroy 1 Machines" is open within 4 seconds
    And I click the "Destroy" button in the dialog "Destroy 1 Machines"
    Then I visit the Machines page
    Then "docker-mayday-test-machine-random" machine should be absent within 60 seconds

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
    And I click the "next" button with id "next"
    Then I input my "GOOGLE_TEST_PASSWORD" in the field with id "Passwd"
    And I press the button with id "signIn"
    When I wait for the dashboard to load
    Then I logout

  @confirm_alert_email
  Scenario: Confirm that alert email arrived
    Then I should receive an email within 200 seconds
