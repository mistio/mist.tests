@scripts
Feature: Scripts

  Background:
    Given I am logged in to mist


  @script-add-ansible
  Scenario Outline: Add ansible script
    When I visit the Scripts page
    And I click the button "+"
    Then I expect the "Script" add form to be visible within max 10 seconds
    When I set the value "TestScript" to field "Script Name" in "script" add form
    And I open the "Type" dropdown in the "script" add form
    And I wait for 1 seconds
    And I click the button "Ansible Playbook" in the "Type" dropdown in the "script" add form
    And I wait for 1 seconds
    And I open the "Source" dropdown in "script" add form
    And I wait for 1 seconds
    And I click the button "Github" in the "Source" dropdown in the "script" add form
    And I set the value "https://github.com/ansible/ansible-examples" to field "Github Repo" the in "script" add form
    And I set the value "blob/master/lamp_simple/site.yml" to field "Entry Point" in the "script" add form
    And I focus on the button "Add" in the "script" add form
    And I expect for the button "Add" in the "script" add form to be clickable within 3 seconds
    And I click the button "Add" in "script" add form
    And I wait for 2 seconds
    When I visit the Scripts page after the counter has loaded
    Then I visit the Home page
    And I wait for the navigation menu to appear
    When I visit the Scripts page
    Then "TestScript" script should be present within 3 seconds


  @script-add
  Scenario Outline: Add script
    And I wait for the navigation menu to appear
    And I visit the Scripts page
    And I click the button "+"
    Then I expect the "Script" add form to be visible within max 10 seconds
    When I set the value "<name>" to field "Script Name" in the "script" add form
    And I open the "Type" dropdown in the "script" add form
    And I wait for 1 seconds
    And I click the "<type>" button in the "Type" dropdown in the "script" add form
    And I wait for 1 seconds
    And I open the "Source" dropdown in the "script" add form
    And I wait for 1 seconds
    And I click the "<source>" button in the "Source" dropdown in the "script" add form
    And I set the value "<script>" to field "<field>" in the "script" add form
    # And I focus on the button "Add" in the "script" add form
    And I expect for the button "Add" in the "script" add form to be clickable within 3 seconds
    And I click the button "Add" in the "script" add form
    And I wait for 2 seconds
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

  @script-tags
  Scenario: Add tags to script
    When I click the "Script1" "script"
    Then I expect the "script" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "script" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove all the previous tags
    And I add a tag with key "first" and value "tag"
    And I add a tag with key "second" and value "tag"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    Then I ensure that the "script" has the tags "first:tag,second:tag" within 5 seconds
    When I click the "Tag" action button in the "script" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    And I ensure that the "script" has the tags "second:tag" within 5 seconds

  @script-delete
  Scenario: Delete script
    When I visit the Scripts page
    Then "Script1" script should be present within 5 seconds
    When I select list item "Script1" script
    And I click the action "Delete" from the script list actions
    And I expect the "Delete Script" dialog to be open within 4 seconds
    And I wait for 2 seconds
    When I click the "Delete" button in the "Delete Script" dialog
    Then I expect the "Delete Script" dialog to be closed within 4 seconds
    And "Script1" script should be absent within 10 seconds
