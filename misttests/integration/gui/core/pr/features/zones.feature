@zones
Feature: Zones

@zone-add
  Scenario: Add a zone
    Given I am logged in to mist
    When I visit the Home page
    Given "GCE" cloud has been added
    When I visit the Zones page
    And I click the button "+"
    Then I expect the "Zone" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "zone" add form
    And I wait for 1 seconds
    And I click the "GCE" button in the "Select Cloud" dropdown in the "zone" add form
    And I set the value "test-zone-random.com." to field "Domain" in the "zone" add form
    Then I expect for the button "Add" in the "zone" add form to be clickable within 5 seconds
    And I click the button "Add" in the "Zone" add form
    Then I expect the "Zone" page to be visible within max 90 seconds
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
    And I click the "DNS" action button in the "cloud" page
    And I wait for 1 seconds
    Then I expect the "DNS option" dialog to be open within 5 seconds
    And I click the "Enabled" toggle button in the "DNS option" dialog
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
    And I click the "DNS" action button in the "cloud" page
    And I wait for 2 seconds
    And I click the "Disabled" toggle button in the "DNS option" dialog
    And I wait for 5 seconds
    And I click the mist logo
    And I wait for 2 seconds
    And I visit the Home page
    And I visit the Zones page
    And I search for "test-zone-random.com."
    Then "test-zone-random.com." zone should be present within 30 seconds
    When I click the "test-zone-random.com." "zone"
    Then I expect the "zone" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "zone" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    Then I ensure that the "zone" has the tags "first:tag,second:tag" within 30 seconds
    When I click the "Tag" action button in the "zone" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    And I wait for 1 seconds
    And I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    And I ensure that the "zone" has the tags "second:tag" within 30 seconds

  @record-add
  Scenario: Add a record
    When I click the fab button in the "zone" page
    Then I expect the "record" add form to be visible within max 5 seconds
    When I open the "Choose Record Type" dropdown in the "record" add form
    And I wait for 1 seconds
    And I click the "A" button in the "Choose Record Type" dropdown in the "record" add form
    And I set the value "test-record-random" to field "Name" in the "record" add form
    And I set the value "1.2.3.4" to field "Rdata" in the "record" add form
    Then I expect for the button "Add" in the "Record" add form to be clickable within 5 seconds
    And I click the button "Add" in the "record" add form
    Then "test-record-random" record should be present within 90 seconds
    And I wait for 1 seconds

  @record-delete
  Scenario: Delete the record created above
    When I select list item "test-record-random" record
    And I click the action "Delete" from the record list actions
    Then I expect the "Delete Record?" dialog to be open within 4 seconds
    And I wait for 1 seconds
    When I click the "Delete" button in the "Delete Record?" dialog
    Then I expect the "Delete Record?" dialog to be closed within 4 seconds
    And "test-record-random" record should be absent within 90 seconds

  @zone-delete
  Scenario: Delete a zone
    When I scroll to the top of the page
    And I click the "Delete" action button in the "zone" page
    Then I expect the "Delete Zone" dialog to be open within 4 seconds
    And I wait for 1 seconds
    When I click the "Delete" button in the "Delete Zone" dialog
    Then I expect the "Delete Zone" dialog to be closed within 4 seconds
    When I visit the Zones page
    And I wait for 2 seconds
    And "test-zone-random.com." zone should be absent within 90 seconds
