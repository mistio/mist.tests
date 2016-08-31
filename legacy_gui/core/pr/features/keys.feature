@keys
Feature: Actions for Keys

  Background:
    Given I am logged in to mist.core
    Given "Azure" cloud has been added

  @key-addition
  Scenario: Add Key
    When I visit the Keys page after the Images counter has loaded
    When I click the button "Add"
    Then I expect for "key-add-popup" popup to appear within max 4 seconds
    When I fill "FirstKey" as key name
    And I click the "Generate" button inside the "Add key" popup
    Then I expect for "key-generate-loader" loader to finish within max 9 seconds
    When I click the "Add" button inside the "Add key" popup
    Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    And I click the button "Home"
    And I expect for "home-page" page to appear within max 4 seconds
    When I visit the Keys page after the counter has loaded
    Then "FirstKey" key should be added within 15 seconds
    Then I click the button "Home"
    And I wait for 1 seconds

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
