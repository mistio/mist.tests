@mayday
Feature: Production

  @add-interval-schedule
  Scenario: Add schedule to be triggered after 5mins
    Given I am logged in to mist.core
    When I visit the Machines page after the counter has loaded
    And I search for "mayday-test"
    Then "mayday-test" machine state has to be "running" within 15 seconds
    When I visit the Schedules page
    And I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "MaydayScheduler" to field "Name" in "schedule" add form
    And I open the "Task" drop down
    And I wait for 1 seconds
    And I click the button "stop" in the "Task" dropdown
    And I wait for 1 seconds
    And I select "Machines with tags" from "ids_or_tags" radio-group
    And I wait for 1 seconds
    And I set the value "mayday-test" to field "Machines with tags" in "schedule" add form
    And I select "Repeat" from "schedule_type" radio-group
    And I set the value "5" to field "interval" in "schedule" add form
    And I click the button "Add" in "schedule" add form
    Then I wait for 2 seconds
    When I visit the Schedules page
    Then "TestScheduler" schedule should be present within 3 seconds

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
