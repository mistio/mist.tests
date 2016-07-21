@keys
Feature: Actions for Keys

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load
#    Given "Azure" cloud has been added

  @key-addition
  Scenario: Add Key
    When I visit the Keys page after the Images counter has loaded
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "FirstKey" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I visit the Keys page after the counter has loaded
    Then "FirstKey" key should be  within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @key-renaming
  Scenario: Rename Key
    When I visit the Keys page after the counter has loaded
    And I click the button "FirstKey"
    And I click the button "Rename"
    Then I expect for "rename-key-popup-popup" popup to appear within max 4 seconds
    When I fill "RenamedFirstKey" as new key name
    And I click the "Save" button inside the "Rename key" popup
    Then I expect for "rename-key-popup-popup" popup to disappear within max 4 seconds
    And I click the button "Keys"
    And I expect for "key-list-page" page to appear within max 4 seconds
    And I click the button "Home"
    And I expect for "home-page" page to appear within max 4 seconds
    When I visit the Keys page after the counter has loaded
    Then "RenamedFirstKey" key should be added within 5 seconds
    Then I click the button "Home"
    And I wait for 1 seconds

  @key-deletion
  Scenario: Delete Key
    When I visit the Keys page after the counter has loaded
    And I click the button "RenamedFirstKey"
    Then I expect for "single-key-page" page to appear within max 4 seconds
    And I click the button "Delete"
    And I expect for "dialog-popup" modal to appear within max 4 seconds
    And I click the button "Yes"
    And I expect for "dialog-popup" modal to disappear within max 4 seconds
    Then "RenamedFirstKey" key should be deleted
    And I wait for 2 seconds
    Then I click the button "Home"
    And I wait for 2 seconds
