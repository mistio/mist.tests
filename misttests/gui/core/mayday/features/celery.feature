Feature: Production-celery-testing

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
