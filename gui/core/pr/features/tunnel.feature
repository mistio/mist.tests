@networks
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
    When I set the value "test_tunnel" to field "Name" in "tunnel" add form
  