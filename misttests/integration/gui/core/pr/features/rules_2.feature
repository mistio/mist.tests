@rules-2
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
    Then "rules-test-machine-random" machine state has to be "running" within 150 seconds
    And I wait for 10 seconds
    When I click the "rules-test-machine-random" "machine"
    And I wait for 2 seconds
    Then "Key1" key should be associated with the machine "rules-test-machine-random" within 120 seconds
    When I click the button "Enable Monitoring" in the "machine" page
    And I wait for 10 seconds
    And I wait for the monitoring graphs to appear in the "machine" page
    Then 5 graphs should be visible within max 30 seconds in the "machine" page

  @metric-rule-rules-page-alert
  Scenario: Insert rule regarding metric from rules page. If triggered, alert
    Given I am logged in to mist
    When I visit the Rules page
    And I click the button "add new rule" in the "rules" page
    And I wait for 1 seconds
    And I select the "machine" apply-on when adding new rule in the "rules" page
    And I select the "select" resource-type when adding new rule in the "rules" page
    And I select the "rules-test-machine-random" resource-id when adding new rule in the "rules" page
    And I select the "metric" target-type when adding new rule in the "rules" page
    And I wait for 5 seconds
    And I select the "system" target when adding new rule in the "rules" page
    And I select the "system.n_cpus" target when adding new rule in the "rules" page
    And I select the "<" operator when adding new rule in the "rules" page
    And I type "9" in the threshold when adding new rule in the "rules" page
    And I select the "every" aggregation when adding new rule in the "rules" page
    And I select the "alert" action when adding new rule in the "rules" page
    And I select the "Owners" team when adding new rule in the "rules" page
    And I wait for 1 seconds
    And I save the new rule in the "rules" page
    And I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    And I scroll to the rules section in the "machine" page
    And I wait for 2 seconds
    Then rule "if system.n_cpus < 9 for every value within 1 minutes then alert team Owners" should be present in the "machine" page
    And I should receive an email at the address "EMAIL" which contains subject terms: "*** WARNING *** machine `rules-test-machine-random`: System" within 180 seconds

  @delete-rule
  Scenario: Delete a rule from rules page and verify it is not visible in single machine page
    When I visit the Rules page
    And I remove previous rules in the "rules" page
    And I wait for 2 seconds
    And I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then rule "if system.n_cpus < 9 for every value within 1 minutes then alert team Owners" should be absent in the "machine" page

  @metric-rule-rules-page-destroy
  Scenario: Add rule from rules section that applies on tagged machine. Verify it is visible in single machine page and it works
    Given I am logged in to mist
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "machine" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "test" and value "awesome"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then I ensure that the "machine" has the tags "test:awesome" within 20 seconds
    When I visit the Rules page
    And I click the button "add new rule" in the "rules" page
    And I wait for 1 seconds
    And I select the "machine" apply-on when adding new rule in the "rules" page
    And I select the "tagged" resource-type when adding new rule in the "rules" page
    And I type "test=awesome" in the tags when adding new rule in the "rules" page
    And I select the "metric" target-type when adding new rule in the "rules" page
    And I wait for 2 seconds
    And I select the "processes" target when adding new rule in the "rules" page
    And I select the "processes.running" target when adding new rule in the "rules" page
    And I select the ">" operator when adding new rule in the "rules" page
    And I type "0" in the threshold when adding new rule in the "rules" page
    And I select the "any" aggregation when adding new rule in the "rules" page
    And I select the "destroy" action when adding new rule in the "rules" page
    And I save the new rule in the "rules" page
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I wait for 1 seconds
    And I click the "rules-test-machine-random" "machine"
    Then rule "if processes.running > 0 for any value then destroy" should be present in the "machine" page
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I wait for 1 seconds
    And "rules-test-machine-random" machine should be absent within 210 seconds
