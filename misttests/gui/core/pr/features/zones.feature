@zones
Feature: Zones

  @zone-add
  Scenario: Add a zone
    Given I am logged in to mist.core
    #Given "GCE" cloud has been added
    When I visit the Zones page
    When I click the "test-zone-14.com." "zone"

  @record-add
  Scenario: Add a record
    Then "test-record-333.test-zone-14.com." record should be present within 10 seconds
    When I select list item "test-record-333.test-zone-14.com." record
    And I click the action "Delete" from the record list actions
  
#  @zone-delete
#  Scenario: Delete a zone
#    When I click the button "Delete" in "zone" edit form
#    Then I expect the dialog "Delete Zone" is open within 4 seconds
#    When I click the "Delete" button in the dialog "Delete Zone"
#    Then I expect the dialog "Delete Zone" is closed within 4 seconds
#    And "test-zone-random.com." zone should be absent within 5 seconds
