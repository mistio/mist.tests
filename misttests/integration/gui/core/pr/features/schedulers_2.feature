@schedulers-2
Feature: Schedulers-b

  @scheduler-requirements
  Scenario: Check state of machines and tag machine that will be used for schedule below
    Given cloud "Docker" has been added via API request
    And key "Key1" has been added via API request
    And Docker machine "test-ui-machine-random" has been added via API request
    And Docker machine "test-ui-machine-2-random" has been added via API request
    Given I am logged in to mist
    And I have given card details if needed
    When I visit the Machines page
    And I wait for 3 seconds
    And I search for "test-ui-machine-random"
    Then "test-ui-machine-random" machine state has to be "running" within 60 seconds
    When I clear the search bar
    And I search for "test-ui-machine-2-random"
    Then "test-ui-machine-2-random" machine state has to be "running" within 10 seconds
    When I click the "test-ui-machine-2-random" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    Then I click the "Tag" action button in the "machine" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "test" and value "awesome"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    When I visit the Machines page after the counter has loaded
    And I clear the search bar
    And I wait for 2 seconds
    And I search for "test-ui-machine-2-random"
    And I click the "test-ui-machine-2-random" "machine"
    Then I ensure that the "machine" has the tags "test:awesome" within 20 seconds
    And I clear the search bar

   @scheduler-add-crontab
   Scenario: Add crontab schedule
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
    And I select the "test-ui-machine-random" checkbox in the "schedule" add form
    And I select the "Crontab" radio button in the "schedule" add form
    #When I set the value "2" to field "Maximum Run Count" in "schedule" add form
    And I set the value "* * * * *" to field "Crontab" in the "schedule" add form
    And I click the button "Add" in the "schedule" add form
    And I wait for 2 seconds
    When I visit the Schedules page
    Then "TestScheduler" schedule should be present within 5 seconds

  @scheduler-run-to-tagged-machine
  Scenario: Run schedule to the machine tagged above
    When I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "TestScheduler_tagged_machine" to field "Name" in the "schedule" add form
    And I open the "Task" dropdown in the "schedule" add form
    And I wait for 1 seconds
    And I click the "stop" button in the "Task" dropdown in the "schedule" add form
    And I wait for 1 seconds
    And I select the "Machines with tags" radio button in the "schedule" add form
    And I wait for 1 seconds
    When I set the value "test=awesome" to field "Machines with tags" in the "schedule" add form
    And I select the "Crontab" radio button in the "schedule" add form
    And I set the value "* * * * *" to field "Crontab" in the "schedule" add form
    And I click the button "Add" in the "schedule" add form
    And I wait for 1 seconds
    And I visit the Schedules page
    Then "TestScheduler_tagged_machine" schedule should be present within 5 seconds

#  @scheduler-add-run-script
#  Scenario: Add a script that will be used for the scheduler
#    Given script "Touchscript" is added
#    When I visit the Schedules page
#    And I click the button "+"
#    Then I expect the "schedule" add form to be visible within max 10 seconds
#    When I set the value "TestScheduler_2" to field "Name" in "schedule" add form
#    And I open the "Task" drop down
#    And I wait for 1 seconds
#    And I click the button "run script" in the "Task" dropdown
#    And I wait for 1 seconds
#    And I open the "Script" drop down
#    And I wait for 1 seconds
#    And I click the button "TestScript" in the "Script" dropdown
#    And I wait for 1 seconds
#    And I select "Specific Machines" from "ids_or_tags" radio-group in "scheduleAddForm"
#    And I wait for 1 seconds
#    And I select the "ui-testing-machine-3" checkbox
#    And I select "Crontab" from "schedule_type" radio-group in "scheduleAddForm"
#    #When I set the value "2" to field "Maximum Run Count" in "schedule" add form
#    And I set the value "*****" to field "Crontab" in "schedule" add form
#    And I click the "run_immediately" button
#    And I click the button "Add" in "schedule" add form
#    And I wait for 1 seconds
#    When I visit the Home page
#    And I visit the Schedules page
#    Then "TestScheduler" schedule should be present within 3 seconds

  @check-machines-state
  Scenario: Check machine's state
    When I visit the Machines page
    And I search for "test-ui-machine-random"
    Then "test-ui-machine-random" machine state has to be "stopped" within 120 seconds
    When I clear the search bar
    And I search for "test-ui-machine-2-random"
    Then "test-ui-machine-2-random" machine state has to be "stopped" within 120 seconds
