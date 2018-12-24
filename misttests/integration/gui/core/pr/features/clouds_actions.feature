@clouds-actions
Feature: Cloud actions for polymer

  Background:
    Given I am logged in to mist

  @cloud-toggle
   Scenario: Toggle a cloud
    Given "Docker" cloud has been added
    When I open the cloud page for "Docker"
    And I click the toggle button in the "cloud" page
    And I wait for 2 seconds
    And I visit the Home page
    And I wait for the navigation menu to appear
    Then cloud "Docker" should be "disabled"
    When I visit the Machines page
    Then "Docker" machine should be absent within 60 seconds
    When I visit the Home page
    And I wait for the navigation menu to appear
    And I open the cloud page for "Docker"
    And I click the toggle button in the "cloud" page
    And I wait for 2 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then cloud "Docker" should be "enabled"
    When I visit the Machines page after the counter has loaded
    And I wait for 1 seconds
    And I search for "Docker"
    And I wait for 1 seconds
    Then "Docker" machine should be present within 60 seconds
    And I visit the Home page

  @cloud-tags
  Scenario: Tag a cloud
    When I open the cloud page for "Docker"
    Then I expect the "cloud" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "cloud" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    Then I ensure that the "cloud" has the tags "first:tag,second:tag" within 5 seconds
    And I wait for 1 seconds
    When I click the "Tag" action button in the "cloud" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    And I ensure that the "cloud" has the tags "second:tag" within 5 seconds

  @cloud-rename
  Scenario: Rename a cloud
    When I click the "Rename" action button in the "cloud" page
    Then I expect the "Rename Cloud" dialog to be open within 4 seconds
    When I set the value "Renamed" to field "Title" in the "Rename Cloud" dialog
    And I wait for 1 seconds
    And I click the "Save Title" button in the "Rename Cloud" dialog
    Then I expect the "Rename Cloud" dialog to be closed within 4 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then "Renamed" cloud has been added

  @cloud-delete
  Scenario: Delete a cloud
    When I open the cloud page for "Renamed"
    Then I expect the "cloud" page to be visible within max 5 seconds
    When I click the "Delete" action button in the "cloud" page
    Then I expect the "Delete Renamed" dialog to be open within 4 seconds
    And I wait for 1 seconds
    And I click the "Delete" button in the "Delete Renamed" dialog
    Then I expect the "Delete Renamed" dialog to be closed within 4 seconds
    And I wait for 2 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I search for "Docker"
    And I wait for 1 seconds
    Then "Docker" machine should be absent within 60 seconds
