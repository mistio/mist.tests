@insights
Feature: Actions for Insights

  @insights-elements-visible
  Scenario: Make sure that insights elements are visible
    Given cloud "Docker" has been added via API request
    And I am logged in to mist
    And I have given card details if needed
    When I visit the Insights page
    And I wait for 2 seconds
    Then the "filtering" section should be visible within 2 seconds
    And the "quick-overview" section should be visible within 2 seconds
    And the "cost_overview" section should be visible within 2 seconds
    And the "graphRow" section should be visible within 2 seconds
    And the "utilization_overview" section should be visible within 2 seconds
    And the "average_load" section should be visible within 2 seconds
    And the "machines_overview" section should be visible within 2 seconds
    And the "machinesCount" section should be visible within 2 seconds

  @cost-and-machine_count-for-docker
  Scenario: Verify that cost and machine count data for docker cloud added above have arrived
    When I refresh the Insights page until data are available
    And I wait for 5 seconds
    Then "cost" in "quick-overview" section should be "$0.00"
    And "machine_count" in "quick-overview" section should be "greater than 0"

  @custom-pricing
  Scenario: Add tag for custom pricing and verify that cost will appear
    When I visit the Machines page
    And I clear the search bar
    And I wait for 2 seconds
    And I search for "unknown"
    And I click the "Docker" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    Then I click the "Tag" action button in the "machine" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "cost_per_month" and value "100"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    When I visit the Machines page
    And I wait for 2 seconds
    And I search for "unknown"
    And I click the "Docker" "machine"
    Then I ensure that the "machine" has the tags "cost_per_month:100" within 20 seconds
    When I visit the Insights page
    And I wait for 60 seconds
    And I refresh the page
    And I wait for 10 seconds
    Then "cost" in "quick-overview" section should be "greater than $0.00"
