@machines-1
Feature: Machines

  Background:
    Given I am logged in to mist

  @key-add
  Scenario: Add script, Docker cloud and key that will be used for ssh access
    Given script "touch_kati" is added via API request
    And cloud "Docker" has been added via API request
    And key "DummyKey" has been added via API request
    And I have given card details if needed
    When I visit the Keys page
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "DummyKey2" to field "Name" in the "key" add form
    And I focus on the button "Generate" in the "key" add form
    And I click the button "Generate" in the "key" add form
    Then I expect for the button "Add" in the "key" add form to be clickable within 22 seconds
    When I focus on the button "Add" in the "key" add form
    And I click the button "Add" in the "key" add form
    Then I expect the "key" page to be visible within max 10 seconds

  @machine-create
  Scenario: Create a machine in Docker provider
    When I visit the Images page
    And I refresh the page
    And I wait for 5 seconds
    Then "mist/ubuntu-14.04:latest" image should be present within 30 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Docker" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "ui-test-create-machine-random" machine
    And I wait for 3 seconds
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I search for "ui-test-create-machine-random"
    Then "ui-test-create-machine-random" machine state has to be "running" within 100 seconds

  @key-associate
  Scenario: Associate key with machine
    When I click the "ui-test-create-machine-random" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Associate Key" action button in the "machine" page
    Then I expect the "Associate a key" dialog to be open within 4 seconds
    And I open the "Select key" dropdown in the "Associate a key" dialog
    And I click the "DummyKey2" button in the "Select key" dropdown in the "Associate a key" dialog
    And I click the "Associate" button in the "Associate a key" dialog
    And I wait for 5 seconds
    Then "DummyKey2" key should be associated with the machine "ui-test-create-machine-random"

  @key-disassociate
  Scenario: Disassociate key
    When I delete the associated key "DummyKey2"
    Then I expect the "Disassociate Key" dialog to be open within 4 seconds
    When I click the "Disassociate" button in the "Disassociate Key" dialog
    And I wait for 2 seconds
    Then there should be 1 keys associated with the machine within 25 seconds

   @machine-run-script
   Scenario: Run script to machine created above
    When I visit the machines page
    And I wait for 2 seconds
    And I search for "ui-test-create-machine-random"
    When I click the "ui-test-create-machine-random" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Run Script" action button in the "machine" page
    Then I expect the "Run a script" dialog to be open within 4 seconds
    And I open the "Select script" dropdown in the "Run a script" dialog
    And I click the "touch_kati" button in the "Select script" dropdown in the "Run a script" dialog
    And I click the "Run script" button in the "Run a script" dialog
    And I wait for 2 seconds

  @machine-shell
  Scenario: Check shell access and verify that script run
    When I visit the Machines page
    And I wait for 2 seconds
    And I search for "ui-test-create-machine-random"
    When I click the "ui-test-create-machine-random" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Shell" action button in the "machine" page
    And I expect terminal to open within 3 seconds
    And shell input should be available after 8 seconds
    And I type in the terminal "ls -l /var"
    And I wait for 1 seconds
    Then dummy_file should be included in the output
    And I close the terminal

  @machine-stop
  Scenario: Stop machine created above and check state
    When I scroll to the top of the page
    And I click the "Stop" action button in the "machine" page
    Then I expect the "Stop Machine" dialog to be open within 4 seconds
    When I click the "Stop" button in the "Stop Machine" dialog
    And I visit the Machines page
    And I wait for 2 seconds
    And I search for "ui-test-create-machine-random"
    Then "ui-test-create-machine-random" machine state has to be "stopped" within 60 seconds

  @machine-destroy
  Scenario: Destroy the machine created
    When I visit the Home page
    And I wait for the navigation menu to appear
    And I visit the Machines page after the counter has loaded
    Then I search for "ui-test-create-machine-random"
    And I wait for 1 seconds
    When I click the "ui-test-create-machine-random" "machine"
    And I clear the search bar
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Destroy" action button in the "machine" page
    And I expect the "Destroy Machine" dialog to be open within 4 seconds
    And I click the "Destroy" button in the "Destroy Machine" dialog
    When I visit the Machines page
    And I search for "ui-test-create-machine-random"
    Then "ui-test-create-machine-random" machine should be absent within 60 seconds
