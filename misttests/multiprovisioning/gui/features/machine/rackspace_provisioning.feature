@rackspace-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @rackspace-machine-create
  Scenario: Create a machine in Rackspace provider, setting expiration date
    Given "Rackspace" cloud has been added
    And I wait for 180 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Rackspace" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "rackspace-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Ubuntu 18.04 LTS (Bionic Beaver) (Cloud)" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "512MB Standard Instance" button in the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Set Expiration" toggle button in the "machine" add form
    And I wait for 1 seconds
    And I set an expiration in "12" "minutes" with a notify of "1" "minutes" before in the "create machine form"
    And I wait for 1 seconds
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "rackspace-mp-test-random"
    Then "rackspace-mp-test-random" machine should be present within 120 seconds
    And I should receive an email at the address "EMAIL" with subject "Machine is about to expire" within 720 seconds
    # When I visit the Machines page
    # And I wait for 1 seconds
    # And I clear the search bar
    # And I search for "rackspace-mp-test-random"
    # Then "rackspace-mp-test-random" machine state has to be "stopped" within 300 seconds
