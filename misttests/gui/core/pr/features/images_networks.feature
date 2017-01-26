@images-networks
Feature: Images and Networks

  Background:
    Given I am logged in to mist.core
    And I am in the new UI

  @image-search
  Scenario: Search image
    When I wait for the dashboard to load
    Given "OpenStack" cloud has been added
    When I visit the Images page
    When I search for "CoreOS"
    Then "CoreOS-Alpha" image should be present within 3 seconds
    And "CoreOS-Beta" image should be present within 3 seconds
    When I search for "CoreOS-Alpha"
    Then "CoreOS-Alpha" image should be present within 3 seconds
    And "CoreOS-Beta" image should be absent within 3 seconds
    When I clear the search bar
    Then "CoreOS-Beta" image should be present within 5 seconds

  @network-add
  Scenario: Add Network
    When I visit the Networks page
    When I click the button "+"
    Then I expect the "network" add form to be visible within max 10 seconds
    When I set the value "network_random" to field "Name" in "network" add form
    Then I open the "Cloud" drop down
    And I wait for 1 seconds
    When I click the button "Openstack" in the "Cloud" dropdown
    And I expect for the button "Add" in "network" add form to be clickable within 3 seconds
    When I focus on the button "Add" in "network" add form
    And I click the button "Add" in "network" add form
    Then I expect the "network" edit form to be visible within max 5 seconds
    When I visit the Networks page
    Then "network_random" network should be present within 20 seconds
    Then I visit the Home page
    When I wait for the dashboard to load

  @network-delete
  Scenario: Delete Network
    When I visit the Networks page
    When I click the "network_random" "network"
    Then I expect for the button "Delete" in "network" edit form to be clickable within 5 seconds
    And I expect the "network" edit form to be visible within max 5 seconds
    Then I click the button "Delete" in "network" edit form
    And I expect the dialog "Delete Network" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Network"
    And I expect the dialog "Delete Network" is closed within 4 seconds
    Then "network_random" network should be absent within 20 seconds
