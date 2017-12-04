@schedulers-1
Feature: Schedulers

  @scheduler-add-interval
  Scenario: Add schedule
    Given cloud "Docker" has been added via API request
    And Docker machine "test-machine-random" has been added via API request
    Given I am logged in to mist.core
    When I visit the Machines page
    And I wait for 3 seconds
    And I search for "test-machine-random"
    Then "test-machine-random" machine state has to be "running" within 60 seconds
    When I visit the Schedules page
    And I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "TestScheduler" to field "Name" in "schedule" add form
    And I open the "Task" drop down
    And I wait for 1 seconds
    And I click the button "stop" in the "Task" dropdown
    And I wait for 1 seconds
    And I select "Specific Machines" from "ids_or_tags" radio-group
    And I wait for 2 seconds
    And I select the "test-machine-random" checkbox
    And I select "Repeat" from "schedule_type" radio-group
    And I set the value "1" to field "interval" in "schedule" add form
    And I click the button "Add" in "schedule" add form
    Then I wait for 2 seconds
    When I visit the Schedules page
    Then "TestScheduler" schedule should be present within 3 seconds

  @scheduler-rename
  Scenario: Rename schedule
    When I click the "TestScheduler" "schedule"
    Then I expect the "schedule" edit form to be visible within max 5 seconds
    When I click the button "Edit" in "schedule" edit form
    Then I expect the dialog "Edit Schedule" is open within 4 seconds
    When I set the value "RenamedSchedule" to field "Name" in "Edit Schedule" dialog
    And I click the "Save" button in the dialog "Edit Schedule"
    And I expect the dialog "Edit Schedule" is closed within 4 seconds
    And I wait for 2 seconds
    When I visit the Schedules page
    Then "TestScheduler" schedule should be absent within 5 seconds
    And "RenamedSchedule" schedule should be present within 5 seconds

  @check-state
  Scenario: Check machine's state
    When I visit the Machines page
    And I search for "test-machine-random"
    Then "test-machine-random" machine state has to be "stopped" within 120 seconds

  @schedule-delete
  Scenario: Delete schedule
    When I visit the Schedules page
    And I click the "RenamedSchedule" "schedule"
    And I click the button "Delete" in "schedule" edit form
    And I expect the dialog "Delete Schedule" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Schedule"
    Then I expect the dialog "Delete Schedule" is closed within 4 seconds
    And I wait for 2 seconds
    When I visit the Schedules page
    Then "RenamedSchedule" schedule should be absent within 5 seconds

  @scheduler-add-run-immediately
  Scenario: Add schedule and run immediately
    When I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "TestScheduler_2" to field "Name" in "schedule" add form
    And I open the "Task" drop down
    And I wait for 1 seconds
    And I click the button "start" in the "Task" dropdown
    And I wait for 1 seconds
    And I select "Specific Machines" from "ids_or_tags" radio-group
    And I wait for 1 seconds
    And I select the "test-machine-random" checkbox
    And I select "Repeat" from "schedule_type" radio-group
    #When I set the value "2" to field "Maximum Run Count" in "schedule" add form
    And I set the value "1" to field "interval" in "schedule" add form
    And I click the "run_immediately" button with id "run_immediately"
    And I click the button "Add" in "schedule" add form
    And I wait for 1 seconds
    When I visit the Home page
    And I wait for 1 seconds
    And I refresh the page
    And I wait for the links in homepage to appear
    And I visit the Schedules page
    Then "TestScheduler_2" schedule should be present within 5 seconds

  @check-machines-state
  Scenario: Check machine's state
    When I visit the Machines page
    And I search for "test-machine-random"
    Then "test-machine-random" machine state has to be "running" within 120 seconds
