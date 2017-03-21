@zones
Feature: Zones

  @zone-add
  Scenario: Add a zone
    Given I am logged in to mist.core
    Given "GCE" cloud has been added
    When I visit the Zones page after the counter has loaded
    When I click the button "+"
    Then I expect the "Zone" add form to be visible within max 10 seconds
    Then I fill in a "zone-random" zone name
    And I open the "Cloud" drop down
    And I wait for 1 seconds
    When I click the button "GCE" in the "Cloud" dropdown
    And I expect for the button "Add" in "Zone" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "Zone" add form
    And I click the button "Add" in "Zone" add form
    Then I expect the "Zone" edit form to be visible within max 20 seconds
    Then I expect the domain "zone-random" to be populated within 300 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @zone-delete
  Scenario: Delete a zone
    Given I am logged in to mist.core
    When I visit the Zones page after the counter has loaded
    Then I click the button "Delete" from the menu of the "zone-random" zone
    And I expect the dialog "Delete Zone" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Zone"
    And I expect the dialog "Delete Zone" is closed within 4 seconds
    Then "zone-random" zone should be absent within 30 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
