@keys
Feature: Actions for Keys

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load
    Given "Azure" cloud has been added
    When I visit the Keys page after the Images counter has loaded

  @key-add
  Scenario: Add Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "FirstKey" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    Then I wait for 5 seconds
    And I click the button "Add" in "key" add form
    When I visit the Keys page after the counter has loaded
    Then "FirstKey" key should be present within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @key-default
  Scenario: Change Default Key
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "SecondKey" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    Then I wait for 5 seconds
    And I click the button "Add" in "key" add form
    When I visit the Keys page after the counter has loaded
    Then "SecondKey" key should be present within 15 seconds
    And I click the button "Make Default" from the menu of the "SecondKey" key
    Then I wait for 1 seconds
    And key "SecondKey" should be default key
    Then I visit the Home page
    When I wait for the dashboard to load

 @key-search
  Scenario: Filter a key
    When I search for "SecondKey"
    Then "FirstKey" key should be absent within 15 seconds
    When I clear the search bar
    Then "FirstKey" key should be present within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

#  @key-rename
#  Scenario: Rename Key
#    When I visit the Keys page after the counter has loaded
#    And I click the button "FirstKey"
#    And I click the button "Rename"
#    Then I expect for "rename-key-popup-popup" popup to appear within max 4 seconds
#    When I fill "RenamedFirstKey" as new key name
#    And I click the "Save" button inside the "Rename key" popup
#    Then I expect for "rename-key-popup-popup" popup to disappear within max 4 seconds
#    And I click the button "Keys"
#    And I expect for "key-list-page" page to appear within max 4 seconds
#    And I click the button "Home"
#    And I expect for "home-page" page to appear within max 4 seconds
#    When I visit the Keys page after the counter has loaded
#    Then "RenamedFirstKey" key should be added within 5 seconds
#    Then I click the button "Home"
#    And I wait for 1 seconds

  @key-tags
  Scenario: Add tags to key
    When I click the "FirstKey" "key"
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
    Then I click the button "Delete" from the menu of the "FirstKey" key
    And I expect the dialog "Delete Key" is open within 4 seconds
    And I click the "Proceed" button in the dialog "Delete Key"
    And I expect the dialog "Delete Key" is closed within 4 seconds
    Then "FirstKey" key should be absent within 15 seconds
    Then I click the button "Delete" from the menu of the "SecondKey" key
    And I expect the dialog "Delete Key" is open within 4 seconds
    And I click the "Proceed" button in the dialog "Delete Key"
    And I expect the dialog "Delete Key" is closed within 4 seconds
    Then "SecondKey" key should be absent within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
