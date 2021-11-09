@azure-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @azure-machine-create
  Scenario: Create a machine in Azure arm provider with new resource group, storage account, network and cloud init
    Given "Microsoft Azure" cloud has been added
    And I wait for 240 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Microsoft Azure" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "arm-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Canonical UbuntuServer 18.04-LTS" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Standard_A1_v2 1 cpus/2.0GB RAM/ 10.0GB SSD" button in the "Size" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "East Asia" button in the "Location" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    Then I set the value "armmptestrandom" to field "Resource Group name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Storage Account name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Network name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Machine Username" in the "machine" add form
    Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "arm-mp-test-random"
    Then "arm-mp-test-random" machine should be present within 120 seconds
    When I wait for 60 seconds
    And I click the "arm-mp-test-random" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    When I wait for 180 seconds
    And I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    Then I expect terminal to open within 30 seconds
    And shell input should be available after 45 seconds
    When I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output
