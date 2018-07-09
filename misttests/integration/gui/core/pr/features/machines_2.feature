@machines-2
Feature: Machines

  Background:
    Given I am logged in to mist.core

  @key-add
  Scenario: Add Docker cloud and key that will be used for ssh access
    Given cloud "Docker" has been added via API request
    And key "DummyKey" has been added via API request

  @add-schedule-on-machine-create
  Scenario: Create a machine in Docker provider and schedule a task to stop the machine immediately
    When I have given card details if needed
    And I visit the Images page
    And I search for "mist/ubuntu-14.04"
    Then "mist/ubuntu-14.04:latest" image should be present within 30 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" drop down
    And I wait for 1 seconds
    And I click the button "Docker" in the "Select Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "ui-test-create-machine-random" machine
    And I wait for 2 seconds
    And I click the "Schedule a task" button with id "app-form-createForm-post_provision_scheduler"
    And I wait for 1 seconds
    And I scroll to the bottom of the page
    And I open the "Schedule Task" drop down
    And I wait for 1 seconds
    And I click the button "Stop" in the "Schedule Task" dropdown
    And I wait for 1 seconds
    And I select "Repeat" from "schedule_type" radio-group in "createForm"
    And I set the value "1" to field "interval" in "machine" add form
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I click the "Launch" button with id "appformsubmit"
    When I visit the Home page
    And I visit the Machines page
    And I search for "ui-test-create-machine-random"
    Then "ui-test-create-machine-random" machine state has to be "running" within 60 seconds
    And "ui-test-create-machine-random" machine state has to be "stopped" within 120 seconds

  @machine-start
  Scenario: Start the machine created above
    When I click the "ui-test-create-machine-random" "machine"
    Then I expect the "machine" edit form to be visible within max 5 seconds
    When I click the button "Start" from the menu of the "machine" edit form
    Then I expect the dialog "Start Machine" is open within 4 seconds
    When I click the "Start" button in the dialog "Start Machine"
    And I visit the Machines page
    And I search for "ui-test-create-machine-random"
    Then "ui-test-create-machine-random" machine state has to be "running" within 60 seconds
