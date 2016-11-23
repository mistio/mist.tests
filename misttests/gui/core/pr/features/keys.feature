@keys
Feature: Actions for Keys

  Background:
    Given I am logged in to mist.core
    When I visit the Keys page

  @key-add
  Scenario: Add Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "Key1" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 5 seconds
    When I visit the Keys page
    Then "Key1" key should be present within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @key-default
  Scenario: Change Default Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "Key2" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 5 seconds
    When I visit the Keys page
    Then "Key2" key should be present within 15 seconds
    And I click the button "Make Default" from the menu of the "Key2" key
    Then I wait for 1 seconds
    And key "Key2" should be default key
    Then I visit the Home page
    When I wait for the dashboard to load

 @key-search
  Scenario: Filter a key
    When I search for "Key2"
    Then "Key1" key should be absent within 15 seconds
    When I clear the search bar
    Then "Key1" key should be present within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @key-rename
  Scenario: Rename Key
    When I click the "Key2" "key"
    And I expect the "key" edit form to be visible within max 5 seconds
    Then I click the button "Rename Key" in "key" edit form
    And I expect the dialog "Rename Key" is open within 4 seconds
    When I set the value "Second" to field "Name" in "Rename Key" dialog
    And I click the "Submit" button in the dialog "Rename Key"
    And I expect the dialog "Rename Key" is closed within 4 seconds
    Then I visit the Keys page
    And "Key2" key should be absent within 5 seconds
    And "Second" key should be present within 5 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @key-tags
  Scenario: Add tags to key
    When I click the "Key1" "key"
    And I expect the "key" edit form to be visible within max 5 seconds
    Then I click the button "Tags" in "key" edit form
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    Then I add a tag with key "first" and value "tag"
    Then I add a tag with key "second" and value "tag"
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
    Then I visit the Home page
    When I wait for the dashboard to load

  @key-delete
  Scenario: Delete Key
    Then I click the button "Delete" from the menu of the "Key1" key
    And I expect the dialog "Delete Key" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Key"
    And I expect the dialog "Delete Key" is closed within 4 seconds
    Then "Key1" key should be absent within 15 seconds
    When I click the "Second" "key"
    And I expect the "key" edit form to be visible within max 5 seconds
    Then I click the button "Delete" in "key" edit form
    And I expect the dialog "Delete Key" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Key"
    And I expect the dialog "Delete Key" is closed within 4 seconds
    Then "Second" key should be absent within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
