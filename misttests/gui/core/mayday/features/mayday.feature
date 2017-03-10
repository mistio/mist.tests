@mayday
Feature: Production

  @graph
  Scenario: Production monitor and graph testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I clear the machines search bar
    Then I wait for the graphs to appear
    And I click the button "Add Graph"
    Then I expect for "selectTarget" modal to appear within max 30 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the popup with id "selectTarget"
    And I wait for 6 seconds
    Then "entropy" graph should appear within 30 seconds
    When I focus on the "entropy" graph
    Then "entropy" graph should have some values
    And I delete the "entropy" graph

  @ssh
  Scenario: Production ssh testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    When I click the mayday machine
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I wait for the graphs to appear
    When I test the ssh connection 2 times for max 100 seconds each time

  @celery
  Scenario: Production machine reboot testing
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    Then I search for the mayday machine
    And I open the actions dialog
    Then I expect for "select-action" modal to appear within max 4 seconds
    When I click the "Reboot" button inside the "select-action" modal
    Then I expect for "confirmation" modal to appear within max 4 seconds
    And I click the button "Reboot"
    Then I expect for "select-action" modal to disappear within max 4 seconds
    And I wait for 4 seconds
    Then Mayday machine state should be "running" within 200 seconds
