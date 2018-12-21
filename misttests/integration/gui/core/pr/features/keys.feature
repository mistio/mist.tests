@keys
Feature: Actions for Keys

  Background:
    Given I am logged in to mist
    When I visit the Keys page

  @key-add
  Scenario: Add Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "TestKey" to field "Name" in the "key" add form
    And I focus on the button "Generate" in the "key" add form
    And I click the button "Generate" in the "key" add form
    Then I expect for the button "Add" in the "key" add form to be clickable within 22 seconds
    When I focus on the button "Add" in the "key" add form
    And I click the button "Add" in the "key" add form
    Then I expect the "key" page to be visible within max 10 seconds
    When I visit the Keys page
    Then "TestKey" key should be present within 15 seconds
    And I visit the Home page
    And I wait for the navigation menu to appear

  @key-default
  Scenario: Change Default Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "Key2" to field "Name" in the "key" add form
    And I click the button "Generate" in the "key" add form
    Then I expect for the button "Add" in the "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in the "key" add form
    And I click the button "Add" in the "key" add form
    Then I expect the "key" page to be visible within max 5 seconds
    When I visit the Keys page
    Then "Key2" key should be present within 15 seconds
    When I select list item "Key2" key
    And I click the action "Make Default" from the key list actions
    And I wait for 1 seconds
    Then key "Key2" should be default key
    And I visit the Home page
    And I wait for the navigation menu to appear

 @key-search
  Scenario: Filter a key
    When I search for "Key2"
    Then "TestKey" key should be absent within 15 seconds
    When I clear the search bar
    Then "TestKey" key should be present within 15 seconds
    And I visit the Home page
    And I wait for the navigation menu to appear

  @key-rename
  Scenario: Rename Key
    When I click the "Key2" "key"
    Then I expect the "key" page to be visible within max 5 seconds
    When I click the "Rename" action button in the "key" page
    Then I expect the "Rename Key" dialog to be open within 4 seconds
    When I set the value "Second" to field "Name" in the "Rename Key" dialog
    And I click the "Submit" button in the "Rename Key" dialog
    Then I expect the "Rename Key" dialog to be closed within 4 seconds
    When I visit the Keys page
    Then "Key2" key should be absent within 5 seconds
    And "Second" key should be present within 5 seconds
    And I visit the Home page
    And I wait for the navigation menu to appear

  @key-tags
  Scenario: Add tags to key
    When I click the "TestKey" "key"
    Then I expect the "key" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "key" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    Then I ensure that the "key" has the tags "first:tag,second:tag" within 5 seconds
    When I click the "Tag" action button in the "key" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    And I ensure that the "key" has the tags "second:tag" within 5 seconds
    And I visit the Home page
    And I wait for the navigation menu to appear

  @key-delete
  Scenario: Delete Key
    When I visit the Keys page
    And I select list item "TestKey" key
    And I click the action "Delete" from the key list actions
    Then I expect the "Delete Key" dialog to be open within 4 seconds
    And I wait for 1 seconds
    When I click the "Delete" button in the "Delete Key" dialog
    And I expect the "Delete Key" dialog to be closed within 4 seconds
    Then "TestKey" key should be absent within 15 seconds
    When I click the "Second" "key"
    Then I expect the "key" page to be visible within max 5 seconds
    When I click the "Delete" action button in the "key" page
    Then I expect the "Delete Key" dialog to be open within 4 seconds
    When I click the "Delete" button in the "Delete Key" dialog
    Then I expect the "Delete Key" dialog to be closed within 4 seconds
    Then "Second" key should be absent within 15 seconds
