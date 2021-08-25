@openstack-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @openstack-machine-create
  Scenario: Create a machine in Openstack provider, with floating ip
    Given "Openstack" cloud has been added
    # make sure resources are populated -- 5mins
    And I wait for 300 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Openstack" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "openstack-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Debian 10.6.1 (x86_64) [2020-10-23]" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "v3-starter-1" button in the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    Then I set the value "public" to field "Networks" in the "machine" add form
    And I wait for 1 seconds
    Then I set the value "SSH" to field "security_group" in the "machine" add form
    And I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "openstack-mp-test-random"
    Then "openstack-mp-test-random" machine should be present within 60 seconds
