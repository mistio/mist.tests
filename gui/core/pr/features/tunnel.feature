@tunnels
Feature: Actions for Tunnels

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load

  @tunnel-add
  Scenario: Add Tunnel
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
    Then I visit the Home page
    When I wait for the dashboard to load
    