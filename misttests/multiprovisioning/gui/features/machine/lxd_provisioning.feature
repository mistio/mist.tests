@lxd-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @lxd-machine-create
  Scenario: Create a machine in lxd
    Given "LXD" cloud has been added
    And I wait for 180 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "LXD" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "lxd-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "imageno1" button in the "Image" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "lxd-mp-test-random"
    Then "lxd-mp-test-random" machine should be present within 120 seconds

  @machine-shell
  Scenario: Check shell access in other server
    When I visit the machines page after the counter has loaded
    And I wait for 10 seconds
    And I click the other server machine
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    When I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    Then I expect terminal to open within 7 seconds
    When I wait for 5 seconds
    And I type in the terminal "ls -l"
    And I wait for 2 seconds
    Then total should be included in the output
    And I close the terminal