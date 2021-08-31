@openstack-provisioning
Feature: Multiprovisioning

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
 
  @openstack-volume-create
  Scenario: Create a volume in Openstack provider
    Given "Openstack" cloud has been added
    And I wait for 180 seconds
    When I visit the Volumes page
    And I clear the search bar
    And I click the button "+"
    Then I expect the "Volume" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I click the "Openstack" button in the "Select Cloud" dropdown in the "volume" add form
    Then I expect the field "Name" in the volume add form to be visible within max 4 seconds
    When I set the value "mp-test-volume-openstack-random" to field "Name" in the "volume" add form
    And I click the button "Add" in the "volume" add form
    And I wait for 5 seconds
    Then "mp-test-volume-openstack-random" volume should be present within 30 seconds
    When I wait for 5 seconds
    And I click the "mp-test-volume-openstack-random" "volume"
    And I expect the "volume" page to be visible within max 5 seconds
    And I wait for 10 seconds
    Then I click the "Delete" action button in the "volume" page
    And I expect the "Delete volume" dialog to be open within 4 seconds
    And I click the "Delete" button in the "Delete volume" dialog
    When I visit the Home page
    And I wait for 2 seconds
    Then I should see a(n) "request" log entry of action "delete_volume" added "a few seconds ago" in the "dashboard" page within 20 seconds
    When I visit the Volumes page
    And I clear the search bar
    And I search for "mp-test-volume-openstack-random"
    Then "mp-test-volume-openstack-random" volume should be absent within 120 seconds
