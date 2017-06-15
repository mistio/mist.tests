@insights
Feature: Actions for Insights

  @insights-elements-visible
  Scenario: Make sure that insights elements are visible
    Given I am logged in to mist.core
    And cloud "Docker" has been added via API request
    And I visit the Insights page
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

  @cost-for-docker
  Scenario: Verify that cost and machine count data for docker cloud added above have arrived
    Then "cost" in "cost_overview" section should be "0"



    # make sure that graph is visible
    # add docker and check cost- it should be 0
    # tag one docker machine with cost_per_month=35
    # make sure that