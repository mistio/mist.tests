@clouds-actions
Feature: Cloud actions for polymer

  Background:
    Given I am logged in to mist.core

  @cloud-edit-creds
  Scenario: AWS cloud added in the beginning, does not have access to list images (DenyDescribeImages policy in aws), whereas the seconds one has (EC2FullAccess)
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request
    Given "AWS" cloud has been added
    When I visit the Images page
    Then "CoreOS stable 1068.8.0 (PV)" image should be absent within 10 seconds
    Then I visit the Home page
    And I wait for the dashboard to load
    When I open the cloud menu for "AWS"
    And  I use my second "AWS" credentials in cloud edit form
    And I focus on the button "Edit Credentials" in "cloud" edit form
    And I click the button "Edit Credentials" in "cloud" edit form
    And I wait for 3 seconds
    And I visit the Images page
    Then "CoreOS stable 1068.8.0 (PV)" image should be present within 20 seconds
    Then I visit the Home page
    And I wait for the links in homepage to appear
    And I expect for "addBtn" to be clickable within max 20 seconds

  @cloud-toggle
   Scenario: Toggle a cloud
    When I open the cloud menu for "Docker"
    And I click the "toggle" button with id "enable-disable-cloud"
    And I wait for 2 seconds
    And I visit the Home page
    And I wait for the links in homepage to appear
    Then cloud "Docker" should be "disabled"
    When I visit the Machines page
    Then "mistcore_debugger_1" machine should be absent within 60 seconds
    When I visit the Home page
    And I wait for the links in homepage to appear
    And I open the cloud menu for "Docker"
    And I click the "toggle" button with id "enable-disable-cloud"
    And I wait for 2 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then cloud "Docker" should be "enabled"
    when I visit the Machines page after the counter has loaded
    And I wait for 1 seconds
    And I search for the machine "mistcore_debugger_1"
    And I wait for 1 seconds
    Then "mistcore_debugger_1" machine should be present within 60 seconds
    And I visit the Home page

  @cloud-rename
  Scenario: Rename a cloud
    Given "Docker" cloud has been added
    Then I open the cloud menu for "Docker"
    When I rename the cloud "Docker" to "Renamed"
    And I click the "save title" button with id "rename-cloud"
    And I wait for 3 seconds
    When I visit the Home page
    And I wait for the dashboard to load
    Then "Renamed" cloud has been added

  @cloud-delete
  Scenario: Delete a cloud
    When I open the cloud menu for "Renamed"
    And I click the "delete cloud" button with id "delete-cloud"
    Then I expect the dialog "Delete Renamed" is open within 4 seconds
    When I click the "Delete" button in the dialog "Delete Renamed"
    Then I expect the dialog "Delete Renamed" is closed within 4 seconds
    And I wait for 2 seconds
    Then I should have 1 clouds added
