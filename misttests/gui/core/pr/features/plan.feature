@plan
Feature: Upgrade plan test

  @upgrade-plan-test
  Scenario: Verify that notification will be shown once machines are more than 5
    #Given cloud "Docker" has been added via API request
    #And cloud "GCE" has been added via API request
    Given I am logged in to mist.core
    When I visit the Account page
    And I wait for 3 seconds
