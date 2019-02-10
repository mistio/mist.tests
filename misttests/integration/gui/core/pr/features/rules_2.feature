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
    Then "rules-test-machine-random" machine state has to be "running" within 120 seconds
    When I click the "rules-test-machine-random" "machine"
    And I wait for 2 seconds
    And I click the button "Enable Monitoring" in the "machine" page
    And I wait for 5 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
    And 5 graphs should be visible within max 30 seconds in the "machine" page

  @add-rule-apply-to-every-machine
  Scenario: Add rule from rules section that applies on all machines. Verify it is visible in single machine page and it works
    When I visit the Rules page
    And I click the button "add new rule" in the "rules" page
    And I wait for 1 seconds
    And I select the "every machine" apply-on when adding new rule in the "rules" page
    And I select the "Load" target when adding new rule in the "rules" page
    And I select the "<" operator when adding new rule in the "rules" page
    And I type "10" in the threshold when adding new rule in the "rules" page
    And I select the "alert" action when adding new rule in the "rules" page
    And I select the "Owners" team when adding new rule in the "rules" page
    And I wait for 1 seconds
    And I save the new rule in the "rules" page
    And I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    And I scroll to the bottom of the page
    And I wait for 2 seconds
    Then rule "if load < 10 for any value then alert team Owners" should be present in the "machine" page
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] *** WARNING *** from rules-test-machine-random: Load" within 150 seconds

@delete-rule
Scenario: Delete a rule from rules page and verify it is not visible in single machine page
    When I visit the Rules page
    When I remove previous rules in the "rules" page
    And I wait for 2 seconds
    And I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then rule "if load < 10 for any value then alert team Owners" should be absent in the "machine" page

@add-rule-apply-to-tagged-machine
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
    And I select the "machines with tag" apply-on when adding new rule in the "rules" page
    And I type "test=awesome" in the tags when adding new rule in the "rules" page
    And I select the "CPU" target when adding new rule in the "rules" page
    And I select the "<" operator when adding new rule in the "rules" page
    And I type "20" in the threshold when adding new rule in the "rules" page
    And I select the "destroy" action when adding new rule in the "rules" page
    And I save the new rule in the "rules" page
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    And I wait for 1 seconds
    And I click the "rules-test-machine-random" "machine"
    Then rule "if cpu < 20 for any value then destroy" should be present in the "machine" page
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    And I clear the search bar
    And I wait for 1 seconds
    And "rules-test-machine-random" machine should be absent within 210 seconds
