@mayday
Feature: Production

  @add-interval-schedule
  Scenario: Add schedule to be triggered after 5mins
    Given I add the MaydaySchedule via api


  @confirm_schedule-triggered
  Scenario: Verify that schedule got triggered
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    And I search for "mayday-test"
    Then "mayday-test" machine state has to be "stopped" within 600 seconds

# set MAYDAY_TOKEN staging
# add docker to tester account
# tag mayday-test
# set MAYDAY_TOKEN mayday
