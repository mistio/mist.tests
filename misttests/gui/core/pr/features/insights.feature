@insights
Feature: Actions for Insights

  @insights-elements-visible
  Scenario: Make sure that insights elements are visible
    Given I am logged in to mist.core
    And I visit the Insights page
    And I wait for 2 seconds
    Then the "quick-overview" section should be visible within 5 seconds
