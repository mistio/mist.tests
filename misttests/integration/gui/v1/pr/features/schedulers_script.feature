@schedulers-script
Feature: Schedulers

  Background:
    Given I am logged in to mist

  @scheduler-initialization
  Scenario: Add Docker cloud,key and script that will be used
    Given cloud "Docker" has been added via API request
    And key "DummyKey" has been added via API request
    And script "Script1" has been added via API request

  @add-scheduled-script-on-machine-create
  Scenario: Create a machine in Docker provider and schedule a task to run a script
    When I have given card details if needed
    And I wait for 15 seconds
    Given Docker machine "test-script-schedule-random" with "DummyKey" key and "Script1" script has been added via API-v2 request
    When I visit the Machines page
    And I wait for 10 seconds
    And I search for "test-script-schedule-random"
    Then "test-script-schedule-random" machine state has to be "running" within 60 seconds
    And I click the "test-script-schedule-random" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    When I wait for 25 seconds
    And I click the "Shell" action button in the "machine" page
    And I wait for 55 seconds
    Then I expect terminal to open within 20 seconds
    And shell input should be available after 30 seconds
    And I type in the terminal "ls -la /var"
    And I wait for 1 seconds
    Then dummy_file should be included in the output