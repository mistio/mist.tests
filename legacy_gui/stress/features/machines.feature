@machines
Feature: Machines

  Background:
    Given I am logged in to mist.core

  @machine-creation
  Scenario: Machine Actions EC2
    Given "EC2" cloud has been added
    When I visit the Machines page after the counter has loaded
    And I click the button "Create Machine"
    Then I expect for "create-machine" panel to appear within max 4 seconds
    When I fill in a "randomly_created" machine name
    And I click the "Select Provider" button inside the "Create Machine" panel
    And I click the "EC2" button inside the "Create Machine" panel
    And I wait for 2 seconds
    And I click button "Select Image" inside "create-machine" when it is clickable within max 5 seconds
    And I click the "Ubuntu Server 14.04 LTS (PV), SSD Volume Type" button inside the "Create Machine" panel
    And I click the "Select Size" button inside the "Create Machine" panel
    And I click the "Micro Instance" button inside the "Create Machine" panel
    And I click the "Select Location" button inside the "Create Machine" panel
    And I click the "ap-northeast-1a" button inside the "Create Machine" panel
    And I click the "Select Key" button inside the "Create Machine" panel
    And I click the "Add Key" button inside the "Create Machine" panel
    Then I expect for "key-add-popup" popup to appear within max 4 seconds
    When I fill "randomly_created_machine_key" as key name
    And I click the "Generate" button inside the "Add key" popup
    Then I expect for "key-generate-loader" loader to finish within max 10 seconds
    When I click the "Add" button inside the "Add key" popup
    Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    When I click the "Enable Monitoring" button inside the "Create Machine" panel
    When I click the "Launch" button inside the "Create Machine" panel
    Then I expect for "create-machine" panel to disappear within max 4 seconds
    And I search for the "randomly_created" Machine
    Then I should see the "randomly_created" machine added within 30 seconds
    And "randomly_created" machine state should be "running" within 400 seconds

    When I choose the "randomly_created" machine
    And I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the "Reboot" button inside the "Actions" popup
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    And "randomly_created" machine state should be "running" within 200 seconds

    When I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the button "Destroy"
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    Then "randomly_created" machine state should be "terminated" within 200 seconds


  @machine-creation-azure
  Scenario: Machine Actions Azure
    Given "Azure" cloud has been added
    When I visit the Machines page after the counter has loaded
    And I click the button "Create Machine"
    Then I expect for "create-machine" panel to appear within max 4 seconds
    When I fill in a "randomly_created" machine name
    And I click the "Select Provider" button inside the "Create Machine" panel
    And I click the "Azure" button inside the "Create Machine" panel
    And I wait for 2 seconds
    And I click button "Select Image" inside "create-machine" when it is clickable within max 5 seconds
    And I click the "Ubuntu Server 14.04 LTS" button inside the "Create Machine" panel
    And I click the "Select Size" button inside the "Create Machine" panel
    And I click the "ExtraSmall" button inside the "Create Machine" panel
    And I click the "Select Location" button inside the "Create Machine" panel
    And I click the "East US" button inside the "Create Machine" panel
    And I click the "Select Key" button inside the "Create Machine" panel
    And I click the "Add Key" button inside the "Create Machine" panel
    Then I expect for "key-add-popup" popup to appear within max 4 seconds
    When I fill "randomly_created_machine_key" as key name
    And I click the "Generate" button inside the "Add key" popup
    Then I expect for "key-generate-loader" loader to finish within max 10 seconds
    When I click the "Add" button inside the "Add key" popup
    Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    When I click the "Enable Monitoring" button inside the "Create Machine" panel
    When I click the "Launch" button inside the "Create Machine" panel
    Then I expect for "create-machine" panel to disappear within max 4 seconds
    And I search for the "randomly_created" Machine
    Then I should see the "randomly_created" machine added within 30 seconds
    And "randomly_created" machine state should be "running" within 400 seconds

    When I choose the "randomly_created" machine
    And I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the "Reboot" button inside the "Actions" popup
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    And "randomly_created" machine state should be "running" within 200 seconds

    When I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the button "Destroy"
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    Then "randomly_created" machine state should be "terminated" within 200 seconds

  @machine-creation-linode
  Scenario: Machine Actions Linode
    Given "Linode" cloud has been added
    When I visit the Machines page after the counter has loaded
    And I click the button "Create Machine"
    Then I expect for "create-machine" panel to appear within max 4 seconds
    When I fill in a "randomly_created" machine name
    And I click the "Select Provider" button inside the "Create Machine" panel
    And I click the "Linode" button inside the "Create Machine" panel
    And I wait for 2 seconds
    And I click button "Select Image" inside "create-machine" when it is clickable within max 5 seconds
    And I click the "Ubuntu 14.04 LTS" button inside the "Create Machine" panel
    And I click the "Select Size" button inside the "Create Machine" panel
    And I click the "Linode 1024" button inside the "Create Machine" panel
    And I click the "Select Location" button inside the "Create Machine" panel
    And I click the "Dallas, TX" button inside the "Create Machine" panel
    And I click the "Select Key" button inside the "Create Machine" panel
    And I click the "Add Key" button inside the "Create Machine" panel
    Then I expect for "key-add-popup" popup to appear within max 4 seconds
    When I fill "randomly_created_machine_key" as key name
    And I click the "Generate" button inside the "Add key" popup
    Then I expect for "key-generate-loader" loader to finish within max 10 seconds
    When I click the "Add" button inside the "Add key" popup
    Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    When I click the "Enable Monitoring" button inside the "Create Machine" panel
    When I click the "Launch" button inside the "Create Machine" panel
    Then I expect for "create-machine" panel to disappear within max 4 seconds
    And I search for the "randomly_created" Machine
    Then I should see the "randomly_created" machine added within 30 seconds
    And "randomly_created" machine state should be "running" within 400 seconds

    When I choose the "randomly_created" machine
    And I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the "Reboot" button inside the "Actions" popup
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    And "randomly_created" machine state should be "running" within 200 seconds

    When I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the button "Destroy"
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    When I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    Then "randomly_created" machine state should be "terminated" within 200 seconds
