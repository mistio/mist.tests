@schedulers_v2
Feature: Schedulers

  @scheduler-add-crontab
  Scenario: Add schedule
    Given I am logged in to mist.core
    And "Docker" cloud has been added
    When I visit the Machines page
    Then "ui-testing-machine-2" machine state has to be "running" within 10 seconds
    When I visit the Schedules page
    And I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "TestScheduler" to field "Name" in "schedule" add form
    And I open the "Task" drop down
    And I wait for 1 seconds
    And I click the button "stop" in the "Task" dropdown
    And I wait for 1 seconds
    And I select "Specific Machines" from "ids_or_tags" radio-group
    And I wait for 1 seconds
    And I select the "ui-testing-machine-2" checkbox
    And I select "Crontab" from "schedule_type" radio-group
    #When I set the value "2" to field "Maximum Run Count" in "schedule" add form
    And I set the value "*****" to field "Crontab" in "schedule" add form
    And I click the button "Add" in "schedule" add form
    And I wait for 1 seconds
    When I visit the Home page
    And I visit the Schedules page
    Then "TestScheduler" schedule should be present within 3 seconds

  @check-machines-state
  Scenario: Check machine's state
    When I visit the Machines page
    Then "ui-testing-machine" machine state has to be "stopped" within 75 seconds


# just check change-schedule
# machines-with tags

# just check starts and expires
# run script


# enable-disable
# schedule with max run
# update -machine (from api-test-1 to api-test-2)