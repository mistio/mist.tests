@rules-2
Feature: Rules

  @add-rule-apply-to-every-machine
  Scenario: Add rule from rules section that applies on all machines. Verify it is visible in single machine page and it works
    Given I am logged in to mist.core
    And cloud "Docker" has been added via API request
    And key "Key1" has been added via API request
    And Docker machine "rules-test-machine-random" has been added via API request
    And I have given card details if needed
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    Then "rules-test-machine-random" machine state has to be "running" within 120 seconds
    When I click the "rules-test-machine-random" "machine"
    And I wait for 2 seconds
    And I click the button "Enable Monitoring"
    And I wait for 5 seconds
    Then I wait for the graphs to appear
    And 9 graphs should be visible within max 30 seconds
    When I visit the Rules page
    And I click the button "add new rule"
    And I wait for 1 seconds
    And I click the "apply on" button with id "apply-on" within "add-new-rule-dialog"
    And I click the "every machine" button in the dropdown with id "apply-on" within "add-new-rule-dialog"
    And I click the "target" button with id "target-0" within "add-new-rule-dialog"
    And I click the "Load" button in the dropdown with id "target-0" within "add-new-rule-dialog"
    And I wait for 1 seconds
    And I click the "<" button in the dropdown with id "operator-0" within "add-new-rule-dialog"
    And I type "10" in input with id "threshold-0" within "add-new-rule-dialog"
    And I click the "actionsDropdown" button with id "actionsDropdown" within "add-new-rule-dialog"
    And I click the "alert" button in the dropdown with id "actionsDropdown" within "add-new-rule-dialog"
    And I open the "teams" mist-dropdown within "add-new-rule-dialog"
    And I select "Owners" in "teams" mist-dropdown within "add-new-rule-dialog"
    And I wait for 2 seconds
    And I save the rule within "add-new-rule-dialog"
    And I visit the Machines page
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    And I scroll to the bottom of the page
    And I wait for 2 seconds
    Then rule "if load < 10 for any value then alert team Owners" should be present
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] *** WARNING *** from rules-test-machine-random: Load" within 150 seconds

@delete-rule
Scenario: Delete a rule from rules page and verify it is not visible in single machine page
    When I visit the Rules page
    And I remove previous rules
    And I wait for 2 seconds
    And I visit the Machines page
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then rule "if load < 10 for any value then alert team Owners" should be absent

@add-rule-apply-to-tagged-machine
 Scenario: Add rule from rules section that applies on tagged machine. Verify it is visible in single machine page and it works
    Given I am logged in to mist.core
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then I expect the "machine" edit form to be visible within max 5 seconds
    When I click the button "Tag" in the "machine" page actions menu
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "test" and value "awesome"
    And I click the button "Save" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then I ensure that the "machine" has the tags "test:awesome" within 20 seconds
    When I visit the Rules page
    And I click the button "add new rule"
    And I wait for 1 seconds
    And I click the "apply on" button with id "apply-on" within "add-new-rule-dialog"
    And I click the "machines with tag" button in the dropdown with id "apply-on" within "add-new-rule-dialog"
    And I type "test=awesome" in input with class name "tags" within "add-new-rule-dialog"
    And I click the "target" button with id "target-0" within "add-new-rule-dialog"
    And I click the "CPU" button in the dropdown with id "target-0" within "add-new-rule-dialog"
    And I wait for 1 seconds
    And I click the "<" button in the dropdown with id "operator-0" within "add-new-rule-dialog"
    And I type "20" in input with id "threshold-0" within "add-new-rule-dialog"
    And I click the "actionsDropdown" button with id "actionsDropdown" within "add-new-rule-dialog"
    And I click the "destroy" button in the dropdown with id "actionsDropdown" within "add-new-rule-dialog"
    And I wait for 1 seconds
    Then I save the rule within "add-new-rule-dialog"
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    And I click the "rules-test-machine-random" "machine"
    Then rule "if cpu < 20 for any value then destroy" should be present
    When I visit the Machines page
    And I search for "rules-test-machine-random"
    And "rules-test-machine-random" machine should be absent within 180 seconds
