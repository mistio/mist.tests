@orchestration
Feature: Tests for orchestration feature

  @template-add
  Scenario: Add a template
    Given I am logged in to mist.core
    When I visit the Templates page
    When I click the button "+"
    Then I expect the "Template" add form to be visible within max 10 seconds
    And I open the "Catalogue Templates" drop down
    And I wait for 1 seconds
    When I click the button "Kubernetes Blueprint" in the "Catalogue Templates" dropdown
    When I set the value "Simple Python Template" to field "Template Name" in "template" add form
    Then I set the value "https://github.com/mistio/simple-python-webserver-blueprint" to field "Github Repo" in "template" add form
    When I set the value "blueprint.yaml" to field "Entry Point" in "template" add form
    And I expect for the button "Add" in "template" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "template" add form
    And I click the button "Add" in "template" add form
    Then I expect the "template" edit form to be visible within max 20 seconds
    When I visit the Home page
    When I wait for the dashboard to load
    When I visit the Templates page
    Then "Simple Python Template" template should be present within 30 seconds
    Then I visit the Home page
    When I wait for the dashboard to load


  @stack-add
  Scenario: First add Docker and key and then create a stack from the template added above
    Given "Docker" cloud has been added
    
    # change below to 'given key has been added...'
    Then I visit the keys page
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "TestKey2" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 15 seconds
    When I visit the Home page
    When I wait for the dashboard to load
    When I visit the Keys page
    Then "TestKey2" key should be present within 15 seconds

    When I visit the Templates page
    And I wait for 2 seconds
    When I click the "Simple Python Template" "template"
    And I expect the "template" edit form to be visible within max 15 seconds
    When I click the button "Create Stack" in "template" edit form
    And I expect the "stack" add form to be visible within max 20 seconds
    When I set the value "Test Stack" to field "Stack Name" in "stack" add form
    And I open the "cloud" drop down
    And I wait for 1 seconds
    And I click the button "Docker" in the "cloud" dropdown
    And I open the "mist image" drop down
    And I wait for 1 seconds
    And I click the button "Debian Wheezy" in the "mist image" dropdown
    And I open the "mist key" drop down
    And I wait for 1 seconds
    And I click the button "TestKey2" in the "mist key" dropdown
    #And I expect for the button "Create Stack" in "stack" add form to be clickable within 9 seconds
    When I focus on the button "Create Stack" in "stack" add form
    And I click the button "Create Stack" in "stack" add form
    Then I expect the "stack" edit form to be visible within max 30 seconds
    When I visit the Home page
    When I wait for the dashboard to load
    When I visit the Stacks page
    Then "Test Stack" stack should be present within 30 seconds


  @template-search
  Scenario: Filter a template
    When I visit the Templates page
    When I search for "Simple Python Template"
    Then "Simple Python Template" template should be present within 15 seconds
    When I clear the search bar
    Then "Simple Python Template" template should be present within 15 seconds
    When I search for "Non-existing Template"
    Then "Simple Python Template" template should be absent within 15 seconds
    When I clear the search bar

  @template-tags
  Scenario: Add tags to template
    When I visit the Templates page
    And I wait for 2 seconds
    When I click the "Simple Python Template" "template"
    And I expect the "template" edit form to be visible within max 5 seconds
    Then I click the button "Tags" in "template" edit form
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    Then I add a tag with key "first" and value "tag"
    Then I add a tag with key "second" and value "tag"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I wait for 2 seconds
    Then I ensure that the "template" has the tags "first:tag,second:tag"
    Then I click the button "Tags" in "template" edit form
    And I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "template" has the tags "second:tag"

  @stack-search
  Scenario: Filter a stack
    When I visit the Stacks page
    When I search for "Test Stack"
    Then "Test Stack" stack should be present within 15 seconds
    When I clear the search bar
    Then "Test Stack" stack should be present within 15 seconds
    When I search for "Non-existing Stack"
    Then "Test Stack" stack should be absent within 15 seconds
    When I clear the search bar
#
#  @stack-tags
#  Scenario: Add tags to stack
#    When I visit the Stacks page
#    And I wait for 1 seconds
#    When I click the "Test Stack" "stack"
#    And I expect the "stack" edit form to be visible within max 5 seconds
#    Then I click the button "Tags" in "stack" edit form
#    And I expect for the tag popup to open within 4 seconds
#    When I remove all the previous tags
#    Then I add a tag with key "first" and value "tag"
#    Then I add a tag with key "second" and value "tag"
#    And I click the button "Save Tags" in the tag menu
#    Then I expect for the tag popup to close within 4 seconds
#    And I wait for 2 seconds
#    Then I ensure that the "stack" has the tags "first:tag,second:tag"
#    Then I click the button "Tags" in "stack" edit form
#    And I expect for the tag popup to open within 4 seconds
#    And I wait for 1 seconds
#    When I remove the tag with key "first"
#    And I wait for 1 seconds
#    And I click the button "Save Tags" in the tag menu
#    Then I expect for the tag popup to close within 4 seconds
#    And I ensure that the "stack" has the tags "second:tag"

  @template-rename
  Scenario: Rename a template
    When I visit the Templates page
    And I wait for 2 seconds
    When I click the "Simple Python Template" "template"
    And I expect the "template" edit form to be visible within max 5 seconds
    Then I click the button "Edit Template" from the menu of the "template" edit form
    And I expect the dialog "Edit Template" is open within 4 seconds
    When I set the value "Renamed Template" to field "Name" in "Edit Template" dialog
    And I click the "Submit" button in the dialog "Edit Template"
    And I expect the dialog "Edit Template" is closed within 4 seconds
    Then I visit the Home page
    Then I visit the templates page
    And "Simple Python Template" template should be absent within 5 seconds
    And "Renamed Template" template should be present within 5 seconds

#  @stack-is-deployed
#  Scenario: Ensure that a stack has been deployed
#    When I visit the Stacks page
#    And I wait for 1 seconds
#    When I click the "TestStack" "stack"
#    Then I ensure that there is at least one machine in the resources list

  @template-delete
  Scenario: Delete a template
    When I visit the Templates page
    When I click the "Renamed Template" "template"
    And I expect the "template" edit form to be visible within max 5 seconds
    Then I click the button "Delete Template" from the menu of the "template" edit form
    And I expect the dialog "Delete Template" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Template"
    And I expect the dialog "Delete Template" is closed within 4 seconds
    Then "Renamed Template" template should be absent within 15 seconds

#  @stack-delete
#  Scenario: Delete a stack
#    When I visit the Stacks page
#    And I wait for 1 seconds
#    When I click the button "Delete" from the menu of the "TestStack" stack
#    And I expect the dialog "Delete Stack" is open within 4 seconds
#    When I click the "Delete" button in the dialog "Delete Stack"
#    Then I expect the dialog "Delete Stack" is closed within 4 seconds
#    And "TestStack" stack should be absent within 5 seconds
