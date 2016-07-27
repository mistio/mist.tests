@scripts
Feature: Scripts

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load
    Given "GCE" cloud has been added
    When I visit the Scripts page after the Images counter has loaded

  @script-add
  Scenario: Add script
    When I click the button "+"
    Then I expect the "Script" add form to be visible within max 10 seconds
    When I set the value "dummyscript" to field "Script Name" in "script" add form
    When I click the button "Executable" in the "Type" dropdown
    And I click the button "Inline" in the "Source" dropdown
    When I set the value "echo bla > ~/kati" to field "Script" in "script" add form
    When I focus on the button "Add" in "script" add form
    And I click the button "Add" in "script" add form
    When I visit the Scripts page after the counter has loaded
    Then "dummyscript" script should be present within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

#  @rename-script
#  Scenario: Rename script
#    Then I click the button "dummyscript"
#    When I click the button "Edit"
#    Then I expect for "script-edit-popup-popup" popup to appear within max 6 seconds
#    When I rename my script with "dummyscriptrenamed" name
#    And I click the button "Save"
#    Then I expect for "script-edit-popup-popup" popup to disappear within max 4 seconds
#    And I click the button "Scripts"
#    Then I should see a script called "dummyscriptrenamed"
#    Then I click the button "Home"
#    And I wait for 1 seconds
#
#  @delete-script
#  Scenario: Delete script
#    And I click the button "dummyscriptrenamed"
#    And I click the button "Delete"
#    Then I expect for "dialog-popup" modal to appear within max 4 seconds
#    And I click the button "Yes"
#    Then I expect for "dialog-popup" modal to disappear within max 4 seconds
#    Then there should be no script called "dummyscriptrenamed"
#    And I wait for 2 seconds
#    Then I click the button "Home"
#    And I wait for 2 seconds
