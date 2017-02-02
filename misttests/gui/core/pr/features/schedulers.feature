@schedulers
Feature: Schedulers

  Background:
    Given I am logged in to mist.core

  @scheduler-add
  Scenario Outline: Add schedule
    When I visit the Schedules page
    When I click the button "+"
    Then I expect the "schedule" add form to be visible within max 10 seconds
    When I set the value "<name>" to field "Name" in "schedule" add form
    And I click the "task_enabled" button
    And I select perform action in schedules add form
    # And I click


    Examples: Schedule according to
    | action  | machines | schedule_type | name     |
    | start   | ba=bi    | Interval      | myInt    |
    # | stop    | co=ci    | Crontab       | myCron   |
    # | reboot  | da=di    | One off       | myOneoff |

  # @scheduler-rename
  # Scenario: Rename schedule
  #   When I click the "myInt" "schedule"
  #   And I expect the "schedule" edit form to be visible within max 5 seconds
  #   Then I click the button "Edit Schedule" from the menu of the "schedule" edit form
  #   And I expect the dialog "Edit Schedule" is open within 4 seconds
  #   When I set the value "SecInt" to field "Name" in "Edit Schedule" dialog
  #   And I click the "Save" button in the dialog "Edit Schedule"
  #   And I expect the dialog "Edit Schedule"  is closed within 4 seconds
  #   Then I visit the schedulers page
  #   And "myInt" schedule should be absent within 5 seconds
  #   And "SecInt" schedule should be present within 5 seconds
  #
  # @schedule-delete
  # Scenario: Delete schedule
  #   When I visit the Schedulers page
  #   Then I click the button "Delete" from the menu of the "SecInt" scheduler
  #   And I expect the dialog "Delete Schedule" is open within 4 seconds
  #   And I click the "Delete" button in the dialog "Delete Scheduler"
  #   And I expect the dialog "Delete Scheduler" is closed within 4 seconds
  #   Then "SecInt" script should be absent within 5 seconds
  #   When I click the "myCron" "script"
  #   And I expect the "scheduler" edit form to be visible within max 5 seconds
  #   Then I click the button "Delete Scheduler" from the menu of the "schedule" edit form
  #   And I expect the dialog "Delete Scheduler" is open within 4 seconds
  #   And I click the "Delete" button in the dialog "Delete Scheduler"
  #   And I expect the dialog "Delete Scheduler" is closed within 4 seconds
  #   Then "myCron" script should be absent within 5 seconds
