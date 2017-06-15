@insights
Feature: Actions for Insights

  @insights-elements-visible
  Scenario: Make sure that insights elements are visible
    Given I am logged in to mist.core
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
    