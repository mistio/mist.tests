@machines
Feature: Machines

  @machine-create
  Scenario: Create a machine in Docker provider and check the ssh connection
    Given I am logged in to mist.core
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
    Then "docker-ui-test-machine-random" machine state has to be "running" within 60 seconds
