@zones
Feature: Zones

  @zone-add
  Scenario: Add a zone
    Given I am logged in to mist.core
    Given "AWS" cloud has been added
    When I visit the Zones page after the counter has loaded
    When I click the button "+"
#    Then I expect the "Template" add form to be visible within max 10 seconds
#    And I open the "Catalogue Templates" drop down
#    And I wait for 1 seconds
#    When I click the button "Kubernetes Blueprint" in the "Catalogue Templates" dropdown
#    When I set the value "Simple Python Template" to field "Template Name" in "template" add form
#    Then I set the value "https://github.com/mistio/simple-python-webserver-blueprint" to field "Github Repo" in "template" add form
#    When I set the value "blueprint.yaml" to field "Entry Point" in "template" add form
#    And I expect for the button "Add" in "template" add form to be clickable within 9 seconds
#    When I focus on the button "Add" in "template" add form
#    And I click the button "Add" in "template" add form
#    Then I expect the "template" edit form to be visible within max 20 seconds
#    When I visit the Home page
#    When I visit the Templates page
#    Then "Simple Python Template" template should be present within 30 seconds
#    Then I visit the Home page
#    When I wait for the dashboard to load
