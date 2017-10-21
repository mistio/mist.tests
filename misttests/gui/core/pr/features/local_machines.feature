@machines-locally
Feature: Machines

  Background:
    Given I am logged in to mist.core

  @machine-requirements
  Scenario: Add script, Docker cloud and key that will be used for ssh access
    Given script "touch_kati" is added via API request
    And cloud "Docker" has been added via API request
    And key "DummyKey" has been added via API request
    When I visit the Keys page
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "DummyKey2" to field "Name" in "key" add form
    And I focus on the button "Generate" in "key" add form
    And I click the button "Generate" in "key" add form
    And I wait for 4 seconds
    Then I expect for the button "Add" in "key" add form to be clickable within 12 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 10 seconds

  @machine-create
  Scenario: Create a machine in Docker provider
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    And I click the button "Docker" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "ui-test-create-machine-random" machine
    And I wait for 3 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I click the "Launch" button with id "appformsubmit"
    Then "ui-test-create-machine-random" machine state has to be "running" within 30 seconds

  @key-associate
  Scenario: Associate key with machine
    When I click the "ui-test-create-machine-random" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Associate Key" from the menu of the "machine" edit form
    Then I expect the dialog "Associate a key" is open within 4 seconds
    And I open the "Select key" drop down
    And I click the button "DummyKey2" in the "Select key" dropdown
    And I click the "Associate" button in the dialog "Associate a key"
    And I wait for 5 seconds
    Then there should be 2 keys associated with the machine
    Then "DummyKey2" key should be associated with the machine "ui-test-create-machine-random"

  @key-disassociate
  Scenario: Disassociate key
    When I delete the associated key "DummyKey2"
    Then I expect the dialog "Disassociate Key" is open within 4 seconds
    When I click the "Disassociate" button in the dialog "Disassociate Key"
    And I wait for 10 seconds
    Then there should be 1 keys associated with the machine

  @machine-stop
  Scenario: Stop machine created above and check state
    When I click the button "Stop" from the menu of the "machine" edit form
    Then I expect the dialog "Stop Machine" is open within 4 seconds
    And I click the "Stop" button in the dialog "Stop Machine"
    Then I visit the Machines page
    Then "ui-test-create-machine-random" machine state has to be "stopped" within 40 seconds

  @machine-start
  Scenario: Start the machine created above
    When I click the "ui-test-create-machine-random" "machine"
    Then I expect the "machine" edit form to be visible within max 5 seconds
    When I click the button "Start" from the menu of the "machine" edit form
    Then I expect the dialog "Start Machine" is open within 4 seconds
    And I click the "Start" button in the dialog "Start Machine"
    Then I visit the Machines page
    Then "ui-test-create-machine-random" machine state has to be "running" within 40 seconds

  @machine-destroy
  Scenario: Destroy the machine created
    When I visit the Home page
    And I wait for the links in homepage to appear
    And I visit the Machines page after the counter has loaded
    Then I search for the machine "ui-test-create-machine-random"
    When I click the "ui-test-create-machine-random" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Destroy" from the menu of the "machine" edit form
    And I expect the dialog "Destroy Machine" is open within 4 seconds
    And I click the "Destroy" button in the dialog "Destroy Machine"
    Then I visit the Machines page
    Then "ui-test-create-machine-random" machine should be absent within 60 seconds
