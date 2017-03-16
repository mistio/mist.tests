Feature: Production-alert-testing

  @alert
  Scenario: Production rule and alert testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I remove previous rules
    When I delete old mayday emails
    And I wait for 2 seconds
    And I focus on the "add new rule" button
    And I click the button "add new rule"
    Then I expect for "newrule" to be visible within max 20 seconds
    And I click the "metricName" rule
#    And I click the "RAM" button in the dropdown with id "metricName"
    When I fill "0" as metric value
    And I save the rule
#    When I remove previous rules
    Then I should receive an email within 200 seconds
