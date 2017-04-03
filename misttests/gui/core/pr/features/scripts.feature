@scripts
Feature: Scripts

  Background:
    Given I am logged in to mist.core

  @script-add
  Scenario Outline: Add script
    When I wait for the dashboard to load
    And I visit the Scripts page
    And I click the button "+"
    Then I expect the "Script" add form to be visible within max 10 seconds
    When I set the value "<name>" to field "Script Name" in "script" add form
    And I open the "Type" drop down
    And I wait for 2 seconds
    And I click the button "<type>" in the "Type" dropdown
    And I wait for 2 seconds
    And I open the "Source" drop down
    And I wait for 2 seconds
    And I click the button "<source>" in the "Source" dropdown
    And I set the value "<script>" to field "<field>" in "script" add form
    And I focus on the button "Add" in "script" add form
    And I expect for the button "Add" in "script" add form to be clickable within 3 seconds
    And I click the button "Add" in "script" add form
    And I wait for 3 seconds
    When I visit the Scripts page after the counter has loaded
    # FIXME: below has been commented out because script is not available immediately..need for redirection to another page first...
    # FIXME: instead of redirecting to home, an option is to sort the items...
    Then I visit the Home page
    And I wait for the dashboard to load
    When I visit the Scripts page
    Then "<name>" script should be present within 3 seconds
    And I visit the Home page


    Examples: Script according to source
    | source        | field       | script                                                                      | name    | type       |
    | Inline        | Script      | #!/bin/bash\necho bla > ~/kati                                              | Script1 | Executable |
    | Github        | Github Repo | https://github.com/ansible/ansible-examples                                 | Script2 | Executable |
    | Url           | Url         | https://github.com/ansible/ansible-examples/blob/master/lamp_simple/site.yml| Script3 | Executable |

  @script-search
  Scenario: Filter scripts
    When I visit the Scripts page
    And I search for "Script1"
    Then "Script2" script should be absent within 5 seconds
    When I clear the search bar
    Then "Script2" script should be present within 5 seconds

  @script-rename
  Scenario: Rename script
    When I click the "Script2" "script"
    Then I expect the "script" edit form to be visible within max 5 seconds
    When I click the button "Edit Script" from the menu of the "script" edit form
    Then I expect the dialog "Edit Script" is open within 4 seconds
    When I set the value "Second" to field "Name" in "Edit Script" dialog
    And I click the "Submit" button in the dialog "Edit Script"
    Then I expect the dialog "Edit Script" is closed within 4 seconds
    When I visit the scripts page
    Then "Script2" script should be absent within 5 seconds
    And "Second" script should be present within 5 seconds

  @script-tags
  Scenario: Add tags to script
    When I click the "Script1" "script"
    Then I expect the "script" edit form to be visible within max 5 seconds
    When I click the button "Tags" in "script" edit form
    Then I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I wait for 2 seconds
    Then I ensure that the "script" has the tags "first:tag,second:tag"
    Then I click the button "Tags" in "script" edit form
    And I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "script" has the tags "second:tag"

  @script-delete
  Scenario: Delete script
    When I visit the Scripts page
    And I click the button "Delete" from the menu of the "Script1" script
    And I expect the dialog "Delete Script" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Script"
    And I expect the dialog "Delete Script" is closed within 4 seconds
    Then "Script1" script should be absent within 5 seconds
    When I click the "Second" "script"
    And I expect the "script" edit form to be visible within max 5 seconds
    And I click the button "Delete Script" from the menu of the "script" edit form
    And I expect the dialog "Delete Script" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Script"
    And I expect the dialog "Delete Script" is closed within 4 seconds
    Then "Second" script should be absent within 5 seconds
