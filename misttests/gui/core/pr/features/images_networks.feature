@images-networks
Feature: Images and Networks

  Background:
    Given I am logged in to mist.core

  @image-search
  Scenario: Search image
    When I expect for "addBtn" to be clickable within max 20 seconds
    Given "OpenStack" cloud has been added
    When I visit the Images page
    And I search for "CoreOS"
    Then "CoreOS-Alpha" image should be present within 3 seconds
    And "CoreOS-Beta" image should be present within 3 seconds
    When I search for "CoreOS-Alpha"
    Then "CoreOS-Alpha" image should be present within 3 seconds
    And "CoreOS-Beta" image should be absent within 3 seconds
    When I clear the search bar
    Then "CoreOS-Beta" image should be present within 5 seconds

  @image-unstar
  Scenario: Unstar image
    When I click the "CoreOS-Beta" "image"
    And I expect the "image" edit form to be visible within max 5 seconds
    Then I click the button "Unstar" in "image" edit form
    Then  I visit the Home page
    And I wait for 2 seconds
    When I visit the Images page
    And I wait for 2 seconds
    Then the "CoreOS-Beta" image should be "unstarred" within 200 seconds

  @image-star
  Scenario: Star image
    When I click the "CoreOS-Beta" "image"
    And I expect the "image" edit form to be visible within max 5 seconds
    Then I click the button "Star" in "image" edit form
    Then  I visit the Home page
    And I refresh the page
    And I wait for the links in homepage to appear
    When I visit the Images page
    And I wait for 2 seconds
    Then the "CoreOS-Beta" image should be "starred" within 200 seconds

  @network-add
  Scenario: Add Network
    When I visit the Networks page
    And I click the button "+"
    Then I expect the "network" add form to be visible within max 10 seconds
    When I set the value "network_random" to field "Name" in "network" add form
    And I open the "Cloud" drop down
    And I wait for 1 seconds
    And I click the button "Openstack" in the "Cloud" dropdown
    Then I expect for the button "Add" in "network" add form to be clickable within 3 seconds
    When I focus on the button "Add" in "network" add form
    And I click the button "Add" in "network" add form
    Then I expect the "network" edit form to be visible within max 5 seconds
    When I visit the Networks page
    Then "network_random" network should be present within 20 seconds

  @network-delete
  Scenario: Delete Network
    When I click the "network_random" "network"
    Then I expect the "network" edit form to be visible within max 5 seconds
    And I expect for the button "Delete" in "network" edit form to be clickable within 5 seconds
    When I click the button "Delete" in "network" edit form
    Then I expect the dialog "Delete Network" is open within 4 seconds
    When I click the "Delete" button in the dialog "Delete Network"
    Then I expect the dialog "Delete Network" is closed within 4 seconds
    When I visit the Home page
    And I visit the Networks page
    Then "network_random" network should be absent within 20 seconds
