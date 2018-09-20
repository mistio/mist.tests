@clouds-actions
Feature: Cloud actions for polymer

  Background:
    Given I am logged in to mist.core

  @cloud-toggle
   Scenario: Toggle a cloud
    Given "Docker" cloud has been added
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

  @cloud-tags
  Scenario: Tag a cloud
    When I open the cloud menu for "Docker"
    Then I expect the "cloud" edit form to be visible within max 5 seconds
    When I click the button "Tag" in "cloud" edit form
    Then I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the button "Save" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "cloud" has the tags "first:tag,second:tag" within 5 seconds
    And I wait for 1 seconds
    When I click the button "Tag" in "cloud" edit form
    Then I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "cloud" has the tags "second:tag" within 5 seconds

  @cloud-rename
  Scenario: Rename a cloud
    When I click the button "Rename" in the "cloud" page actions menu
    Then I expect the dialog "Rename Cloud" is open within 4 seconds
    Then I set the value "Renamed" to field "TITLE" in "Rename Cloud" app-form dialog
    And I wait for 1 seconds
    And I focus on the button "Save Title" in "cloud" edit form
    And I click the button "Save Title" in "cloud" edit form
    And I wait for 3 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then "Renamed" cloud has been added

  @cloud-delete
  Scenario: Delete a cloud
    When I open the cloud menu for "Renamed"
    Then I expect the "cloud" edit form to be visible within max 5 seconds
    When I click the button "Delete" in the "cloud" page actions menu
    Then I expect the dialog "Delete Renamed" is open within 4 seconds
    And I wait for 1 seconds
    And I focus on the button "Delete" in "cloud" edit form
    And I click the button "Delete" in "cloud" edit form
    Then I expect the dialog "Delete Renamed" is closed within 4 seconds
    And I wait for 2 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I search for the machine "mistcore_debugger_1"
    And I wait for 1 seconds
    Then "mistcore_debugger_1" machine should be absent within 60 seconds
