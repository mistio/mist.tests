@machines
Feature: Machines

  Scenario: Create machine from machine list

    Given I am logged in to mist.core
    Given "EC2" cloud has been added
    And I wait for 5 seconds
    When I visit the machines page
    #When I visit the Machines page after the Images counter has loaded
    And I wait for 5 seconds
    And I click the button "Create Machine"
    Then I expect for "create-machine" panel to appear within max 4 seconds
    When I fill in a "random first" machine name
    And I click the "Select Provider" button inside the "Create Machine" panel
    And I click the "EC2" button inside the "Create Machine" panel
    And I click the "Select Image" button inside the "Create Machine" panel
    And I click the "Ubuntu Server" button inside the "Create Machine" panel
    And I click the "Select Size" button inside the "Create Machine" panel
    And I click the "Micro Instance" button inside the "Create Machine" panel
    And I click the "Select Location" button inside the "Create Machine" panel
    And I click the "ap-northeast-1a" button inside the "Create Machine" panel
    And I click the "Select Key" button inside the "Create Machine" panel
    And I click the "Add Key" button inside the "Create Machine" panel
    Then I expect for "key-add-popup" popup to appear within max 4 seconds
    When I fill "first_machine_key" as key name
    And I click the "Generate" button inside the "Add key" popup
    Then I wait until the private key is generated
    When I click the "Add" button inside the "Add key" popup
    Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    And I click the button "Enable Monitoring"
    When I click the "Launch" button inside the "Create Machine" panel
    Then I expect for "create-machine" panel to disappear within max 4 seconds
    Then I search for the "first" Machine

    Then I should see the "first" machine added within 200 seconds

    Then "first" machine state should be "running" within 200 seconds

    And I click the button "first"
    Then I expect for "single-machine-page" page to appear within max 5 seconds
    When I click the button "Tags"
    Then I expect for "machine-tags-popup-popup" popup to appear within max 10 seconds
    And I remove all the previous tags
    When I name a "testkey" key and a "testvalue" value for a tag
    And I click the button "Save tags"
    Then I expect for "machine-tags-popup-popup" popup to disappear within max 20 seconds
    When I check if the "testkey" key and "testvalue" value appear for the machine
    Then I wait for 1 seconds
    And I click the button "Tags"
    Then I expect for "machine-tags-popup-popup" popup to appear within max 10 seconds
    When I click the button "Add Item"
    And I name a "sectestkey" key and a "sectestvalue" value for a tag
    And I click the button "Save Tags"
    Then I expect for "machine-tags-popup-popup" popup to disappear within max 20 seconds
    When I check if the "sectestkey" key and "sectestvalue" value appear for the machine
    And I click the button "Tags"
    Then I expect for "machine-tags-popup-popup" popup to appear within max 10 seconds
    And I close the tag with key "sectestkey"
    When I click the button "Save Tags"
    Then I expect for "machine-tags-popup-popup" popup to disappear within max 20 seconds
    When I focus on the "Machines" button
    Then I click the button "Machines"
    When I clear the machines search bar
    Then I search for the "first" Machine
    And I wait for 5 seconds
    # WONTFIX in Ember.js
    #Then the "first" machine in the list should have a tag with key "testkey" and value "testvalue"

    And I click the button "first"
    And I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the "Destroy" button inside the "Actions" popup
    Then I expect for "dialog-popup" modal to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" modal to disappear within max 4 seconds
    Then I click the button "Machines"

    When I clear the machines search bar
    Then I search for the "first" Machine
    And I wait for 1 seconds
    And "first" machine state should be "terminated" within 200 seconds

    When I click the button "Home"
    Then I expect for "home-page" page to appear within max 4 seconds
    When I visit the Keys page after the counter has loaded
    When I click the button "first_machine_key"
    Then I expect for "single-key-page" page to appear within max 4 seconds
    When I click the button "Delete"
    Then I expect for "dialog-popup" modal to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" modal to disappear within max 4 seconds
    Then I wait for 2 seconds
    And "first_machine_key" key should be deleted
