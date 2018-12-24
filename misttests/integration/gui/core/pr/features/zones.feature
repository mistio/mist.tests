@zones
Feature: Zones

@zone-add
  Scenario: Add a zone
    Given I am logged in to mist
    When I visit the Home page
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given "GCE" cloud has been added
    When I visit the Zones page
    And I click the button "+"
    Then I expect the "Zone" add form to be visible within max 10 seconds
    When I open the "Select Cloud" drop down
    And I wait for 1 seconds
    And I click the button "GCE" in the "Select Cloud" dropdown
    And I set the value "test-zone-random.com." to field "Domain" in "Zone" add form
    Then I expect for the button "Add" in "Zone" add form to be clickable within 5 seconds
    When I focus on the button "Add" in "Zone" add form
    And I click the button "Add" in "Zone" add form
    Then I expect the "Zone" edit form to be visible within max 60 seconds
    And I visit the Zones page
    And I search for "test-zone-random.com."
    Then "test-zone-random.com." zone should be present within 60 seconds

  @zone-search
  Scenario: Filter a zone
    When I clear the search bar
    Then "test-zone-random.com." zone should be present within 10 seconds
    When I search for "Non-existing zone"
    Then "test-zone-random.com." zone should be absent within 10 seconds
    When I clear the search bar
    And I wait for 1 seconds

  @disable-dns-support
  Scenario: Disable dns support and verify that zone created above is not visible
    When I visit the Home page
    And I wait for 1 seconds
    And I open the cloud page for "GCE"
    And I click the button "DNS" in "cloud" edit form
    And I wait for 1 seconds
    And I click the "Enable DNS" button with id "DNS-enable-disable"
    And I wait for 5 seconds
    And I click the mist logo
    And I wait for 2 seconds
    And I visit the Home page
    And I visit the Zones page
    Then "test-zone-random.com." zone should be absent within 10 seconds

  @zone-tags
  Scenario: Reenable dns-support and add tags to a zone
    When I visit the Home page
    And I wait for 1 seconds
    And I open the cloud page for "GCE"
    And I click the button "DNS" in "cloud" edit form
    And I wait for 2 seconds
    And I click the "Enable DNS" button with id "DNS-enable-disable"
    And I wait for 5 seconds
    And I click the mist logo
    And I wait for 2 seconds
    And I visit the Home page
    And I visit the Zones page
    And I search for "test-zone-random.com."
    Then "test-zone-random.com." zone should be present within 30 seconds
    When I click the "test-zone-random.com." "zone"
    Then I expect the "zone" edit form to be visible within max 5 seconds
    When I click the button "Tag" in "zone" edit form
    Then I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the button "Save" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "zone" has the tags "first:tag,second:tag" within 25 seconds
    When I click the button "Tag" in "zone" edit form
    And I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    And I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "zone" has the tags "second:tag" within 5 seconds

  @record-add
  Scenario: Add a record
    When I click the button "+"
    Then I expect the "record" add form to be visible within max 5 seconds
    When I open the "Choose Record Type" drop down
    And I wait for 1 seconds
    And I click the button "A" in the "Choose Record Type" dropdown
    And I set the value "test-record-random" to field "Name" in "record" add form
    And I set the value "1.2.3.4" to field "Rdata" in "record" add form
    Then I expect for the button "Add" in "Record" add form to be clickable within 5 seconds
    When I focus on the button "Add" in "Record" add form
    And I click the button "Add" in "record" add form
    Then "test-record-random" record should be present within 30 seconds
    And I wait for 1 seconds

  @record-delete
  Scenario: Delete the record created above
    When I select list item "test-record-random" record
    And I click the action "Delete" from the record list actions
    Then I expect the dialog "Delete Record?" is open within 4 seconds
    And I wait for 1 seconds
    When I click the "Delete" button in the dialog "Delete Record?"
    Then I expect the dialog "Delete Record?" is closed within 4 seconds
    And "test-record-random" record should be absent within 30 seconds

  @zone-delete
  Scenario: Delete a zone
    When I scroll to the element with id "wrapper"
    And I click the button "Delete" in the "zone" page actions menu
    Then I expect the dialog "Delete Zone" is open within 4 seconds
    And I wait for 1 seconds
    When I click the "Delete" button in the dialog "Delete Zone"
    Then I expect the dialog "Delete Zone" is closed within 4 seconds
    When I visit the Zones page
    And I wait for 2 seconds
    And "test-zone-random.com." zone should be absent within 60 seconds
