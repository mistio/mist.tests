@scripts
Feature: Scripts

  Background:
    Given I am logged in to mist.core
    And I am in the legacy UI
    Given "GCE" cloud has been added
    #When I visit the Scripts page after the Images counter has loaded
    When I visit the Scripts page

  @create-script
  Scenario: Add script
    And I click the button "Add Script"
    Then I expect for "add-script" panel to appear within max 4 seconds
    And I wait for 1 seconds
    Then I type "dummyscript" in input with id "script-name"
    When I click the "Select Source" button inside the "Add Script" panel
    And I click the "Inline" button inside the "Add Script" panel
    And I write "echo bla > ~/kati" in the script textfield
    And I click the button "Add"
    Then I expect for "add-script" panel to disappear within max 4 seconds
    And I should see a script called "dummyscript"
    Then I click the button "Home"
    And I wait for 1 seconds

  @rename-script
  Scenario: Rename script
    Then I click the button "dummyscript"
    When I click the button "Edit"
    Then I expect for "script-edit-popup-popup" popup to appear within max 6 seconds
    When I rename my script with "dummyscriptrenamed" name
    And I click the button "Save"
    Then I expect for "script-edit-popup-popup" popup to disappear within max 4 seconds
    And I click the button "Scripts"
    Then I should see a script called "dummyscriptrenamed"
    Then I click the button "Home"
    And I wait for 1 seconds

  @delete-script
  Scenario: Delete script
    And I click the button "dummyscriptrenamed"
    And I click the button "Delete"
    Then I expect for "dialog-popup" modal to appear within max 4 seconds
    And I click the button "Yes"
    Then I expect for "dialog-popup" modal to disappear within max 4 seconds
    Then there should be no script called "dummyscriptrenamed"
    And I wait for 2 seconds
    Then I click the button "Home"
    And I wait for 2 seconds
