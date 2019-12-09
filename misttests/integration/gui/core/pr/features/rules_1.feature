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
    Then "Key1" key should be associated with the machine "rules-test-machine-random" within 120 seconds
    When I click the button "Enable Monitoring" in the "machine" page
    And I wait for 5 seconds
    And I wait for the monitoring graphs to appear in the "machine" page
    Then 5 graphs should be visible within max 30 seconds in the "machine" page

  @metric-rule-machine-page-alert
  Scenario: Insert rule regarding metric from machine page. If triggered, alert
    When I scroll to the rules section in the "machine" page
    And I wait for 1 seconds
    And I click the button "add new rule" in the "machine" page
    And I wait for 1 seconds
    And I select the "metric" target-type when adding new rule in the "machine" page
    And I select the "RAM" target when adding new rule in the "machine" page
    And I select the ">" operator when adding new rule in the "machine" page
    And I type "0" in the threshold when adding new rule in the "machine" page
    And I select the "any" aggregation when adding new rule in the "machine" page
    And I select the "alert" action when adding new rule in the "machine" page
    And I select the "Owners" team when adding new rule in the "machine" page
    And I wait for 2 seconds
    And I save the new rule in the "machine" page

  # @log-rule-rules-page-alert
  # Scenario: Insert rule regarding log from rules page. If triggered, alert
  #   When I visit the Rules page
  #   And I click the button "add new rule" in the "rules" page
  #   And I wait for 1 seconds
  #   And I select the "cloud" apply-on when adding new rule in the "rules" page
  #   And I select the "all" resource-type when adding new rule in the "rules" page
  #   And I select the "log" target-type when adding new rule in the "rules" page
  #   And I type "type:request AND action:create_machine" in the target when adding new rule in the "rules" page
  #   And I select the ">" operator when adding new rule in the "rules" page
  #   And I type "0" in the threshold when adding new rule in the "rules" page
  #   And I select the "alert" action when adding new rule in the "rules" page
  #   And I select the "Owners" team when adding new rule in the "rules" page
  #   And I wait for 1 seconds
  #   And I save the new rule in the "rules" page
  #   And I wait for 3 seconds

  @incidents-triggered
  Scenario: Verify that incidents get triggered
    Given Docker machine "rules-test-machine-1-random" has been added via API request
    When I visit the Home page
    And I wait for the navigation menu to appear
    And I open the cloud page for "Docker"
    And I wait for 1 seconds
    Then I should see a(n) "request" log entry of action "create_machine" added "a few seconds ago" in the "cloud" page within 20 seconds
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-1-random"
    Then "rules-test-machine-1-random" machine should be present within 60 seconds
    #And I should receive an email at the address "EMAIL" with subject "*** WARNING *** from : count of matching logs" within 150 seconds
    And I should receive an email at the address "EMAIL" with subject "[Mist.io] *** WARNING *** from rules-test-machine-random: RAM" within 180 seconds

  @metric-rule-machine-page-destroy
  Scenario: Insert rule regarding metric from machine page. If triggered, destroy the machine
    When I visit the Rules page
    And I click the button "add new rule" in the "rules" page
    And I wait for 1 seconds
    And I select the "machine" apply-on when adding new rule in the "rules" page
    And I select the "all" resource-type when adding new rule in the "rules" page
    And I select the "metric" target-type when adding new rule in the "machine" page
    And I select the "Load" target when adding new rule in the "machine" page
    And I select the "<" operator when adding new rule in the "machine" page
    And I type "1" in the threshold when adding new rule in the "machine" page
    And I select the "any" aggregation when adding new rule in the "machine" page
    And I select the "destroy" action when adding new rule in the "machine" page
    And I wait for 2 seconds
    And I save the new rule in the "machine" page
    And I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-random"
    Then "rules-test-machine-random" machine state has to be "running" within 30 seconds
    And "rules-test-machine-random" machine should be absent within 180 seconds
