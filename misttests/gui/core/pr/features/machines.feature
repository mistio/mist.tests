@machines
Feature: Machines

  Background:
    Given I am logged in to mist.core


  @machine-create
  Scenario: Create a machine in Docker provider and check the ssh connection
    And "Docker" cloud has been added
    When I refresh the page
    And I wait for the dashboard to load
    And I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    And I click the button "Docker" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "docker-ui-test-machine-random" machine
    And I wait for 3 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I wait for 2 seconds
    And I click the "Launch" button with id "appformsubmit"
    And I wait for 5 seconds
    Then "docker-ui-test-machine-random" machine state has to be "running" within 100 seconds

  @machine-destroy
  Scenario: Destroy the machine created
    When I visit the Home page
    And I wait for the dashboard to load
    And I visit the Machines page after the counter has loaded
    Then I search for the machine "docker-ui-test-machine-random"
    When I click the "docker-ui-test-machine-random" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Destroy" from the menu of the "machine" edit form
    And I expect the dialog "Destroy 1 Machines" is open within 4 seconds
    And I click the "Destroy" button in the dialog "Destroy 1 Machines"
    Then I visit the Machines page
    Then "docker-ui-test-machine-random" machine should be absent within 60 seconds

  @machine-shell
  Scenario: Check shell access
    When I visit the Machines page
    Then I search for the machine "api_test_machine_3"
    When I click the "api_test_machine_3" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Shell" from the menu of the "machine" edit form
