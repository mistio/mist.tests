@tunnels
Feature: Actions for Tunnels

  Background:
    Given I am logged in to mist.core
    And I am in the new UI

  @tunnel-add
  Scenario: Add Tunnel
    When I wait for the dashboard to load
    When I visit the Tunnels page
    When I click the button "+"
    Then I expect the "tunnel" add form to be visible within max 10 seconds
    When I set the value "test_tunnel" to field "Tunnel Name" in "tunnel" add form
    And I set the value "172.17.1.0/24" to field "CIDRS" in "tunnel" add form
    And I expect for the button "Add" in "tunnel" add form to be clickable within 3 seconds
    When I focus on the button "Add" in "tunnel" add form
    And I click the button "Add" in "tunnel" add form
    Then I expect the "tunnel" edit form to be visible within max 5 seconds
    When I visit the Tunnels page
    Then "test_tunnel" tunnel should be present within 30 seconds

  @tunnel-tags
  Scenario: Add tags to tunnel
    When I click the "test_tunnel" "tunnel"
    And I expect the "tunnel" edit form to be visible within max 5 seconds
    Then I click the button "Tags" in "tunnel" edit form
    And I expect for the tag popup to open within 4 seconds
    When I remove all the previous tags
    Then I add a tag with key "test" and value "tag"
    And I click the button "Save Tags" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I wait for 2 seconds
    Then I ensure that the "tunnel" has the tags "test:tag"

  @tunnel-delete
  Scenario: Delete Tunnel
    When I visit the Tunnels page
    Then I click the "test_tunnel" "tunnel"
    And I expect the "tunnel" edit form to be visible within max 5 seconds
    Then I click the button "Delete Tunnel" from the menu of the "tunnel" edit form
    And I expect the dialog "Delete Tunnel" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Tunnel"
    And I expect the dialog "Delete Tunnel" is closed within 4 seconds
    Then I visit the Home page
    When I visit the Tunnels page
    Then "test_tunnel" tunnel should be absent within 30 seconds
