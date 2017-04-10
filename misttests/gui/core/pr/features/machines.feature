@machines
Feature: Machines

  Background:
    Given I am logged in to mist.core

  @key-add
  Scenario: Add Key that will be used for ssh access
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given "Docker" cloud has been added
    When I visit the Keys page
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "Key1" to field "Name" in "key" add form
    And I focus on the button "Generate" in "key" add form
    And I click the button "Generate" in "key" add form
    And I wait for 4 seconds
    Then I expect for the button "Add" in "key" add form to be clickable within 12 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 10 seconds

  @key-associate
  Scenario: Associate key with machine
    When I visit the machines page
    When I click the "machine2-ui-testing" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Associate Key" from the menu of the "machine" edit form
    Then I expect the dialog "Associate a key" is open within 4 seconds
    And I open the "Select key" drop down
    And I click the button "Key1" in the "Select key" dropdown
    And I click the "Associate" button in the dialog "Associate a key"
    And I wait for 2 seconds
    Then there should be 1 keys associated with the machine
    Then "Key1" key should be associated with the machine "machine2-ui-testing"

  @key-disassociate
  Scenario: Disassociate key
    When I delete the associated key
    Then I expect the dialog "Disassociate Key" is open within 4 seconds
    When I click the "Disassociate" button in the dialog "Disassociate Key"
    And I wait for 5 seconds
    Then there should be 0 keys associated with the machine

  @machine-create
  Scenario: Create a machine in Docker provider
    When I visit the Home page
    And I refresh the page
    And I wait for the links in homepage to appear
    When I visit the Machines page
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

  @script-add
  Scenario: Add script
    When I visit the Scripts page
    And I click the button "+"
    Then I expect the "Script" add form to be visible within max 10 seconds
    When I set the value "Script1" to field "Script Name" in "script" add form
    And I open the "Type" drop down
    And I wait for 2 seconds
    And I click the button "Executable" in the "Type" dropdown
    And I wait for 2 seconds
    And I open the "Source" drop down
    And I wait for 2 seconds
    And I click the button "Inline" in the "Source" dropdown
    And I set the value "#!/bin/bash\ntouch /temp/kati" to field "Script" in "script" add form
    And I focus on the button "Add" in "script" add form
    And I expect for the button "Add" in "script" add form to be clickable within 3 seconds
    And I click the button "Add" in "script" add form
    And I wait for 3 seconds
    When I visit the Scripts page after the counter has loaded
    Then I visit the Home page
    And I wait for the links in homepage to appear
    When I visit the Scripts page
    Then "Script1" script should be present within 3 seconds
    And I visit the Home page

  @machine-shell
  Scenario: Check shell access
    When I click the "docker-ui-test-machine-random" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Shell" from the menu of the "machine" edit form
    And I test the ssh connection
    And I wait for 1 seconds

  @machine-stop
  Scenario: Stop machine created above and check state
    When I click the button "Stop" from the menu of the "machine" edit form
    Then I expect the dialog "Stop 1 Machines" is open within 4 seconds
    And I click the "Stop" button in the dialog "Stop 1 Machines"
    Then I visit the Machines page
    Then "docker-ui-test-machine-random" machine state has to be "stopped" within 30 seconds

  @machine-start
  Scenario: Start the machine created above
    When I click the "docker-ui-test-machine-random" "machine"
    Then I expect the "machine" edit form to be visible within max 5 seconds
    When I click the button "Start" from the menu of the "machine" edit form
    Then I expect the dialog "Start 1 Machines" is open within 4 seconds
    And I click the "Start" button in the dialog "Start 1 Machines"
    Then I visit the Machines page
    Then "docker-ui-test-machine-random" machine state has to be "running" within 30 seconds

  @machine-destroy
  Scenario: Destroy the machine created
    When I visit the Home page
    And I wait for the links in homepage to appear
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
