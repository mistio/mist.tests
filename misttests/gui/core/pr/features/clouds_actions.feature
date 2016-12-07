@clouds-actions
Feature: Cloud actions for polymer

  Background:
    Given I am logged in to mist.core
    And I am in the new UI

  @cloud-edit-creds
  Scenario Outline: Edit credentials of a cloud
    When I wait for the dashboard to load
    Given "Openstack" cloud has been added
    When I visit the Machines page
    Then "Test" machine should be absent within 15 seconds
    Then I open the cloud menu for "Openstack"
    And  I use my second "<provider>" credentials in cloud edit form
    And I focus on the button "Edit Credentials" in "cloud" edit form
    Then I click the button "Edit Credentials" in "cloud" edit form
    And I wait for 5 seconds
    # stin openstack o admin exei 1 machine, enw o tester den exei

  Examples: Providers
  | provider       |
  | Packet         |

  @cloud-rename
  Scenario: Rename a cloud
    Given "Openstack" cloud has been added
    Then I open the cloud menu for "Openstack"
    When I rename the cloud "Openstack" to "Renamed"
    And I click the "save title" button
    And I wait for 3 seconds
    #When I click the mist-logo
    When I visit the Home page
    And I wait for the dashboard to load
    Then "Renamed" cloud has been added


  @cloud-delete
  Scenario: Delete a cloud
    Given "Renamed" cloud has been added
    Then I open the cloud menu for "Renamed"
    And I click the "delete cloud" button
    And I wait for 2 seconds
    Then the "Renamed" cloud should be deleted