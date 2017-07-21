@keys
Feature: Actions for Keys

  Background:
    Given I am logged in to mist.core
    When I visit the Keys page

  @key-add
  Scenario: Add Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "TestKey" to field "Name" in "key" add form
    And I focus on the button "Generate" in "key" add form
    And I click the button "Generate" in "key" add form
    And I wait for 7 seconds
    Then I expect for the button "Add" in "key" add form to be clickable within 12 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 10 seconds
    When I visit the Keys page
    Then "TestKey" key should be present within 15 seconds
    And I visit the Home page
    And I wait for the links in homepage to appear

  @key-default
  Scenario: Change Default Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "Key2" to field "Name" in "key" add form
    And I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    Then I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 5 seconds
    When I visit the Keys page
    Then "Key2" key should be present within 15 seconds
    When I select list item "Key2" key
    And I click the action "Make Default" from the key list actions
    And I wait for 1 seconds
    Then key "Key2" should be default key
    And I visit the Home page
    And I wait for the links in homepage to appear

 @key-search
  Scenario: Filter a key
    When I search for "Key2"
    Then "TestKey" key should be absent within 15 seconds
    When I clear the search bar
    Then "TestKey" key should be present within 15 seconds
    And I visit the Home page
    And I wait for the links in homepage to appear

  @key-rename
  Scenario: Rename Key
    When I click the "Key2" "key"
    Then I expect the "key" edit form to be visible within max 5 seconds
    When I click the button "Rename Key" in "key" edit form
    Then I expect the dialog "Rename Key" is open within 4 seconds
    When I set the value "Second" to field "Name" in "Rename Key" dialog
    And I click the "Submit" button in the dialog "Rename Key"
    Then I expect the dialog "Rename Key" is closed within 4 seconds
    When I visit the Keys page
    Then "Key2" key should be absent within 5 seconds
    And "Second" key should be present within 5 seconds
    And I visit the Home page
    And I wait for the links in homepage to appear

  @key-tags
  Scenario: Add tags to key
    When I click the "TestKey" "key"
    Then I expect the "key" edit form to be visible within max 5 seconds
    When I click the button "Tags" in "key" edit form
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I wait for 2 seconds
    Then I ensure that the "key" has the tags "first:tag,second:tag"
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

  @key-delete
  Scenario: Delete Key
    When I visit the Keys page
    And I select list item "Second" key
    And I select list item "TestKey" key
    And I click the action "Delete" from the key list actions
    Then I expect the dialog "Delete Key" is open within 4 seconds
    And I wait for 2 seconds
    When I click the "Delete" button in the dialog "Delete Key"
    And I expect the dialog "Delete Key" is closed within 4 seconds
    Then "TestKey" key should be absent within 15 seconds
    When I click the "Second" "key"
    And I expect the "key" edit form to be visible within max 5 seconds
    Then I click the button "Delete" in "key" edit form
    And I expect the dialog "Delete Key" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Key"
    And I expect the dialog "Delete Key" is closed within 4 seconds
    Then "Second" key should be absent within 15 seconds
