@schedulers-1
Feature: Schedulers

  @scheduler-add-interval
  Scenario: Add schedule
    Given cloud "Docker" has been added via API request
    And key "Key1" has been added via API request
    And Docker machine "test-machine-random" has been added via API request
    Given I am logged in to mist
    And I have given card details if needed
    When I visit the Machines page
    And I wait for 3 seconds
    And I search for "test-machine-random"
    Then "test-machine-random" machine state has to be "running" within 60 seconds
    When I visit the Schedules page
    And I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "TestScheduler" to field "Name" in the "schedule" add form
    And I open the "Task" dropdown in the "schedule" add form
    And I wait for 1 seconds
    And I click the "stop" button in the "Task" dropdown in the "schedule" add form
    And I wait for 1 seconds
    And I select the "Specific Machines" radio button in the "schedule" add form
    And I wait for 2 seconds
    And I select the "test-machine-random" checkbox in the "schedule" add form
    And I select the "Repeat" radio button in the "schedule" add form
    And I set the value "1" to field "interval" in the "schedule" add form
    And I set the value "2" to field "Maximum Run Count" in the "schedule" add form
    And I click the button "Add" in the "schedule" add form
    Then I wait for 2 seconds
    When I visit the Schedules page
    Then "TestScheduler" schedule should be present within 3 seconds

  @scheduler-rename
  Scenario: Rename schedule
    When I click the "TestScheduler" "schedule"
    Then I expect the "schedule" page to be visible within max 5 seconds
    When I click the "Edit" action button in the "schedule" page
    Then I expect the "Edit Schedule" dialog to be open within 4 seconds
    When I set the value "RenamedSchedule" to field "Name" in the "Edit Schedule" dialog
    And I click the "Save" button in the "Edit Schedule" dialog
    And I expect the "Edit Schedule" dialog to be closed within 4 seconds
    And I wait for 2 seconds
    When I visit the Schedules page
    Then "TestScheduler" schedule should be absent within 5 seconds
    And "RenamedSchedule" schedule should be present within 5 seconds

  @check-state
  Scenario: Check machine's state
    When I visit the Machines page
    And I clear the search bar
    And I wait for 2 seconds
    And I search for "test-machine-random"
    Then "test-machine-random" machine state has to be "stopped" within 120 seconds

  @schedule-delete
  Scenario: Delete schedule
    When I visit the Schedules page
    And I click the "RenamedSchedule" "schedule"
    And I click the "Delete" action button in the "schedule" page
    And I expect the "Delete Schedule" dialog to be open within 4 seconds
    And I click the "Delete" button in the "Delete Schedule" dialog
    Then I expect the "Delete Schedule" dialog to be closed within 4 seconds
    And I wait for 2 seconds
    When I visit the Schedules page
    Then "RenamedSchedule" schedule should be absent within 5 seconds

  @scheduler-add-run-immediately
  Scenario: Add schedule and run immediately
    When I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "TestScheduler_2" to field "Name" in the "schedule" add form
    And I open the "Task" dropdown in the "schedule" add form
    And I wait for 1 seconds
    And I click the "start" button in the "Task" dropdown in the "schedule" add form
    And I wait for 1 seconds
    And I select the "Specific Machines" radio button in the "schedule" add form
    And I wait for 1 seconds
    And I select the "test-machine-random" checkbox in the "schedule" add form
    And I select the "Repeat" radio button in the "schedule" add form
    #When I set the value "2" to field "Maximum Run Count" in "schedule" add form
    And I set the value "1" to field "interval" in the "schedule" add form
    And I click the "Run once immediately" toggle button in the "schedule" add form
    And I click the button "Add" in the "schedule" add form
    And I wait for 5 seconds
    # When I visit the Home page
    # And I wait for 1 seconds
    # And I refresh the page
    # And I wait for the navigation menu to appear
    And I visit the Schedules page
    Then "TestScheduler_2" schedule should be present within 5 seconds

  @check-machines-state
  Scenario: Check machine's state
    When I visit the Machines page
    And I clear the search bar
    And I wait for 2 seconds
    And I search for "test-machine-random"
    Then "test-machine-random" machine state has to be "running" within 120 seconds
