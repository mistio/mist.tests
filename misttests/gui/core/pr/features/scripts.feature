@scripts
Feature: Scripts

  Background:
    Given I am logged in to mist.core

  @script-add
  Scenario Outline: Add script
    And I wait for the links in homepage to appear
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

  @script-delete
  Scenario: Delete script
    When I visit the Scripts page
    And I click the button "Delete" from the menu of the "Script1" script
    And I expect the dialog "Delete Script" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Script"
    And I expect the dialog "Delete Script" is closed within 4 seconds
    Then "Script1" script should be absent within 5 seconds
