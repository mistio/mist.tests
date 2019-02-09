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
    And 5 graphs should be visible within max 30 seconds in the "machine" page

  @alert-email
  Scenario: Insert rule that will be triggered immediately
    When I click the button "add new rule" in the "machine" page
    And I wait for 1 seconds
    And I select the "RAM" target when adding new rule in the "machine" page
    And I select the ">" operator when adding new rule in the "machine" page
    And I type "0" in the threshold when adding new rule in the "machine" page
    And I select the "alert" action when adding new rule in the "machine" page
    And I select the "Owners" team when adding new rule in the "machine" page
    And I wait for 2 seconds
    And I save the new rule in the "machine" page

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
    And I expect the "machine" page to be visible within max 5 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
    When I remove previous rules in the "machine" page
    And I click the button "add new rule" in the "machine" page
    And I wait for 1 seconds
    And I select the "Load" target when adding new rule in the "machine" page
    And I select the "<" operator when adding new rule in the "machine" page
    And I type "10" in the threshold when adding new rule in the "machine" page
    And I select the "destroy" action when adding new rule in the "machine" page
    And I wait for 2 seconds
    And I save the new rule in the "machine" page
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    Then "rules-test-machine-random" machine state has to be "running" within 30 seconds
    And "rules-test-machine-random" machine should be absent within 180 seconds
