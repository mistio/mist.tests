@clouds-actions
Feature: Cloud actions for polymer

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
            And I click the sign in button in the landing page popup


  @cloud-edit-creds
  Scenario: Edit credentials of a cloud
    When I wait for the dashboard to load
    Given "Openstack" cloud has been added
    When I visit the Networks page
    Then "private_network" network should be present within 10 seconds
    Then I visit the Home page
    And I wait for the dashboard to load
    Then I open the cloud menu for "Openstack"
    And  I use my second "Openstack" credentials in cloud edit form
    And I focus on the button "Edit Credentials" in "cloud" edit form
    Then I click the button "Edit Credentials" in "cloud" edit form
    And I wait for 5 seconds
    When I visit the Networks page
    Then "private_network" network should be absent within 10 seconds
    Then I visit the Home page
    And I wait for the dashboard to load

  @cloud-toggle
   Scenario: Toggle a cloud
    Given "Docker" cloud has been added
    Then I open the cloud menu for "Docker"
    When I click the "toggle" button
    And I wait for 2 seconds
    When I visit the Home page
    And I wait for the dashboard to load
    Then cloud "Docker" should be "disabled"
    When I visit the Machines page
    Then "yolomachine" machine should be absent within 120 seconds
    Then I visit the Home page
    And I wait for the dashboard to load
    When I open the cloud menu for "Docker"
    And I click the "toggle" button
    And I wait for 2 seconds
    When I visit the Home page
    And I wait for the dashboard to load
    Then cloud "Docker" should be "enabled"
    When I visit the Machines page
    Then "yolomachine" machine should be present within 120 seconds
    Then I visit the Home page

  @cloud-rename
  Scenario: Rename a cloud
    Given "Docker" cloud has been added
    Then I open the cloud menu for "Docker"
    When I rename the cloud "Docker" to "Renamed"
    And I click the "save title" button
    And I wait for 3 seconds
    When I visit the Home page
    And I wait for the dashboard to load
    Then "Renamed" cloud has been added

  @cloud-delete
  Scenario: Delete a cloud
    Then I open the cloud menu for "Renamed"
    And I click the "delete cloud" button
    And I wait for 2 seconds
    Then the "Renamed" cloud should be deleted
