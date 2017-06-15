@insights
Feature: Actions for Insights

  @insights-elements-visible
  Scenario: Make sure that insights elements are visible
    Given cloud "Docker" has been added via API request
    And I am logged in to mist.core
    When I visit the Insights page
    And I wait for 2 seconds
    Then the "filtering" section should be visible within 2 seconds
    And the "quick-overview" section should be visible within 2 seconds
    And the "cost_overview" section should be visible within 2 seconds
    And the "run_rate" section should be visible within 2 seconds
    And the "utilization_overview" section should be visible within 2 seconds
    And the "average_load" section should be visible within 2 seconds
    And the "machines_overview" section should be visible within 2 seconds
    And the "machinesCount" section should be visible within 2 seconds
    And the "machinesList" section should be visible within 2 seconds

  @cost-and-machine_count-for-docker
  Scenario: Verify that cost and machine count data for docker cloud added above have arrived
    When I refresh the Insights page until data are available
    Then "cost" in "quick-overview" section should be "$0.00"
    And "machine_count" in "quick-overview" section should be "greater than 0"

  @custom-pricing
  Scenario: Add tag for custom pricing and verify cost
    When I visit the Machines page
    And I wait for 2 seconds
    And I click the "testerrr" "machine"
    Then I expect the "machine" edit form to be visible within max 5 seconds
    Then I click the button "Tag" from the menu of the "machine" edit form
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "cost_per_moth" and value "50"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    When I visit the Machines page
    And I click the "testerrr" "machine"
    And I wait for 5 seconds
    Then I ensure that the "machine" has the tags "cost_per_moth:50"



    # make sure that cost will be greater than before (or specifically 35?) (step:4)


    # make sure that graph is visible
    # add second cloud with existing machines
    # make sure that cost will be higher
    # filter by cloud, make sure that cost will be the same as step 4
