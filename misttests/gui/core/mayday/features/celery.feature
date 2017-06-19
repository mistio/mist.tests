@mayday-celery
Feature: Production

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
    And I wait for 40 seconds
    And I open the actions dialog
    Then I expect for "select-action" modal to appear within max 4 seconds
    When I click the "Shell" button inside the "select-action" modal
    And I expect terminal to open within 3 seconds
    And I wait for 5 seconds
    And I type in the terminal "uptime"
    And I wait for 1 seconds
    Then up 0 min should be included in the output
    And I close the terminal
    And I wait for 1 seconds
