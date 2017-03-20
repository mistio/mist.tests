@zones
Feature: Zones

  @zone-add
  Scenario: Add a zone
    Given I am logged in to mist.core
    Given "AWS" cloud has been added
    When I visit the Zones page after the counter has loaded
    When I click the button "+"
    Then I expect the "Zone" add form to be visible within max 10 seconds
    Then I fill in a "zone-random" zone name
    And I open the "Cloud" drop down
    And I wait for 1 seconds
    When I click the button "AWS" in the "Cloud" dropdown
    And I expect for the button "Add" in "Zone" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "Zone" add form
    And I click the button "Add" in "Zone" add form
    Then I expect the "Zone" edit form to be visible within max 20 seconds
    When I visit the Home page
    When I visit the Zones page
    Then "zone-random" zone should be present within 30 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
