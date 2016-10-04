@orchestration
Feature: Tests for orchestration feature
  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load
    When I visit the Templates page

  @template-add
  Scenario: First add the template that will later be used
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
    Then I expect the "template" edit form to be visible within max 10 seconds
    When I visit the Templates page
    Then "Simple Python Template" template should be present within 10 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
   # Then I visit the Stacks page

 @template-search
 Scenario: Filter a template
    When I search for "Simple Python Template"
    Then "Simple Python Template" template should be present within 15 seconds
    When I clear the search bar
    Then "Simple Python Template" template should be present within 15 seconds
    When I search for "Non-existing Template"
    Then "Simple Python Template" template should be absent within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @template-tags
    Scenario: Add tags to template
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
    Then I ensure that the "Simple Python Template" has the tags "first:tag,second:tag"
    Then I click the button "Tags" in "template" edit form
    And I expect for the tag popup to open within 4 seconds
    And I wait for 1 seconds
    When I remove the tag with key "first"
    And I wait for 1 seconds
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "key" has the tags "second:tag"
    Then I visit the Home page
    When I wait for the dashboard to load
