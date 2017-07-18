@zones
Feature: Zones

  @zone-add
  Scenario: Add a zone
    Given I am logged in to mist.core
    And cloud "GCE" has been added via API request
    When I visit the Zones page
    And I click the button "+"
    Then I expect the "Zone" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    And I click the button "GCE" in the "Choose Cloud" dropdown
    And I set the value "test-zone-random.com." to field "Domain" in "Zone" add form
    Then I expect for the button "Add" in "Zone" add form to be clickable within 5 seconds
    When I focus on the button "Add" in "Zone" add form
    And I click the button "Add" in "Zone" add form
    Then I expect the "Zone" edit form to be visible within max 5 seconds
    When I visit the Zones page
    Then "test-zone-random.com." zone should be present within 5 seconds

  @zone-tags
  Scenario: Add tags to a zone
    When I click the "test-zone-random.com." "zone"
    Then I expect the "zone" edit form to be visible within max 5 seconds
    When I click the button "Tags" in "zone" edit form
    Then I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I wait for 2 seconds
    And I ensure that the "key" has the tags "first:tag,second:tag"


    Then I click the button "Tags" in "key" edit form
    And I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "key" has the tags "second:tag"
    And I visit the Home page
    And I wait for the links in homepage to appear

#    Then I expect the domain "zone-random" to be populated within 300 seconds
#    Then I visit the Home page
#    When I wait for the dashboard to load
#
#  @zone-delete
#  Scenario: Delete a zone
#    Given I am logged in to mist.core
#    When I visit the Zones page after the counter has loaded
#    Then I click the button "Delete" from the menu of the "zone-random" zone
#    And I expect the dialog "Delete Zone" is open within 4 seconds
#    And I click the "Delete" button in the dialog "Delete Zone"
#    And I expect the dialog "Delete Zone" is closed within 4 seconds
#    Then "zone-random" zone should be absent within 30 seconds
#    Then I visit the Home page
#    When I wait for the dashboard to load
