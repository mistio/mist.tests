@orchestration
Feature: Tests for orchestration feature
  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    Then I visit the Home page
    When I wait for the dashboard to load

  @template-add
  Scenario: Add a template
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
    Then I visit the templates page
    And "Simple Python Template" template should be absent within 5 seconds
    And "Renamed Template" template should be present within 5 seconds

  @template-delete
  Scenario: Delete a template
    When I visit the Templates page
    When I click the "Simple Python Template" "template"
    And I expect the "template" edit form to be visible within max 5 seconds
    Then I click the button "Delete Template" from the menu of the "template" edit form
    And I expect the dialog "Delete Template" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Template"
    And I expect the dialog "Delete Template" is closed within 4 seconds
    Then "Simple Python Template" template should be absent within 15 seconds

  @stack-add
  Scenario: First add the template that will later be used in order to create a stack
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
    When I click the button "Create Stack" in "template" edit form
    And I expect the "stack" add form to be visible within max 20 seconds
    When I set the value "TestStack" to field "Stack Name" in "stack" add form
    And I expect for the button "Create Stack" in "stack" add form to be clickable within 9 seconds
    When I focus on the button "Create Stack" in "stack" add form
    And I click the button "Create Stack" in "stack" add form
    Then I expect the "stack" edit form to be visible within max 30 seconds


  @stack-search
  Scenario: Filter a stack
    When I visit the Stacks page
    When I search for "TestStack"
    Then "TestStack" stack should be present within 15 seconds
    When I clear the search bar
    Then "TestStack" stack should be present within 15 seconds
    When I search for "Non-existing Stack"
    Then "TestStack" stack should be absent within 15 seconds
    When I clear the search bar

  @stack-tags
  Scenario: Add tags to stack
    When I visit the Stacks page
    And I wait for 1 seconds
    When I click the "TestStack" "stack"
    And I expect the "stack" edit form to be visible within max 5 seconds
    Then I click the button "Tags" in "stack" edit form
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    Then I add a tag with key "first" and value "tag"
    Then I add a tag with key "second" and value "tag"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I wait for 2 seconds
    Then I ensure that the "stack" has the tags "first:tag,second:tag"
    Then I click the button "Tags" in "stack" edit form
    And I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "stack" has the tags "second:tag"
