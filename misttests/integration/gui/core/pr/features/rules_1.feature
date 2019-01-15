@rules-1
Feature: Rules

  @enable-monitoring
  Scenario: Create Machine, deploy monitoring agent by clicking 'Enable monitoring' button and check the graphs
    Given I am logged in to mist
    And cloud "Docker" has been added via API request
    And I have given card details if needed
    And key "Key1" has been added via API request
    And Docker machine "rules-test-machine-random" has been added via API request
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    Then "rules-test-machine-random" machine state has to be "running" within 120 seconds
    When I click the "rules-test-machine-random" "machine"
    And I wait for 2 seconds
    And I click the button "Enable Monitoring" in the "machine" page
    And I wait for 5 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
    And 9 graphs should be visible within max 30 seconds in the "machine" page

  @alert-email
  Scenario: Insert rule that will be triggered immediately
    When I click the button "add new rule" in the "machine" page
    And I wait for 1 seconds
    And I click the "RAM" button in the dropdown with id "target-0" within "add-new-rule-dialog"
    And I click the ">" button in the dropdown with id "operator-0" within "add-new-rule-dialog"
    And I type "0" in input with id "threshold-0" within "add-new-rule-dialog"
    And I click the "actionsDropdown" button with id "actionsDropdown" within "add-new-rule-dialog"
    And I click the "alert" button in the dropdown with id "actionsDropdown" within "add-new-rule-dialog"
    And I open the "teams" mist-dropdown within "add-new-rule-dialog"
    And I select "Owners" in "teams" mist-dropdown within "add-new-rule-dialog"
    And I wait for 2 seconds
    And I save the rule within "add-new-rule-dialog"

  @incidents
  Scenario: Verify that incident gets triggered
    #When I wait for 55 seconds
    #And I visit the home page
    #And I refresh the page
    #And I wait for 5 seconds
    #Then I should see the incident "RAM > 0.0%"
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] *** WARNING *** from rules-test-machine-random: RAM" within 150 seconds

  @alert-destroy-machine
  Scenario: Insert rule that will kill the container
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I scroll to the element with id "add-new-rule-dialog"
    And I remove previous rules
    And I click the button "add new rule"
    And I wait for 1 seconds
    And I click the "Load" button in the dropdown with id "target-0" within "add-new-rule-dialog"
    And I click the "<" button in the dropdown with id "operator-0" within "add-new-rule-dialog"
    And I type "10" in input with id "threshold-0" within "add-new-rule-dialog"
    And I click the "actionsDropdown" button with id "actionsDropdown" within "add-new-rule-dialog"
    And I click the "destroy" button in the dropdown with id "actionsDropdown" within "add-new-rule-dialog"
    And I wait for 2 seconds
    Then I save the rule within "add-new-rule-dialog"
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    Then "rules-test-machine-random" machine state has to be "running" within 30 seconds
    And "rules-test-machine-random" machine should be absent within 180 seconds
