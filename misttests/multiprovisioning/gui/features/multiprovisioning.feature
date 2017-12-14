@multi-provisioning
Feature: Multiprovisioning testing against prod. Stager account is used.

  Background:
    Given I am logged in to mist.core

  @mp-test
  Scenario Outline: Create a machine, enable monitoring and then destroy it.
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    And I click the button "<provider>" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "mp-test-machine-random" to field "Machine Name" in "machine" add form
    When I open the "Image" drop down
    And I click the button "<image>" in the "Image" dropdown
    And I open the "Key" drop down
    And I click the button "DummyKey" in the "Key" dropdown
    And I wait for 1 seconds
    When I open the "Size" drop down
    And I click the button "<size>" in the "Size" dropdown
    When I open the "Location" drop down
    And I click the button "<location>" in the "Location" dropdown
    And I wait for 2 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I click the "Launch" button with id "appformsubmit"
    When I visit the Home page
    And I visit the Machines page
    And I search for "mp-test-machine-random"
    Then "mp-test-machine-random" machine state has to be "running" within 60 seconds

    # enable monitoring
    When I click the "mp-test-machine-random" "machine"
    And I wait for 2 seconds
    And I click the button "Enable Monitoring"
    And I wait for 2 seconds
    Then I wait for the graphs to appear
    And 9 graphs should be visible within max 30 seconds

    # disable monitoring
    When I visit the Machines page
    And I click the "mp-test-machine-random" "machine"
    And I wait for 2 seconds
    And I click the "Disable Monitoring" button with id "monitoring-menu-wrapper"
    And I wait for 2 seconds
    And I click the "Disable Monitoring" button with id "monitoring-menu-wrapper"
    Then I expect the dialog "Disable Machine Monitoring" is open within 5 seconds
    When I click the "Disable Monitoring" button in the dialog "Disable Machine Monitoring"
    Then I expect the dialog "Disable Machine Monitoring" is closed within 5 seconds
    And graphs should disappear within 15 seconds

    # destroy the machine
    When I visit the Machines page after the counter has loaded
    Then I search for the machine "mp-test-machine-random"
    And I wait for 1 seconds
    When I click the "mp-test-machine-random" "machine"
    And I clear the machines search bar
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Destroy" from the menu of the "machine" edit form
    And I expect the dialog "Destroy Machine" is open within 4 seconds
    And I click the "Destroy" button in the dialog "Destroy Machine"
    When I visit the Machines page
    And I search for "mp-test-machine-random"
    Then "mp-test-machine-random" machine should be absent within 60 seconds

    Examples: Providers to be tested
    | provider      | size  | location    | image              |
    | Digital Ocean | 512mb | Amsterdam 2 | Ubuntu 14.04.5 x64 |
#    | GCE           |
