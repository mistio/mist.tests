@volumes-provisioning
Feature: Multiprovisioning

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear

  @mp-test-create-volume
  Scenario Outline: Create a volume in various providers
    Given "<cloud>" cloud has been added
    And I wait for 40 seconds
    When I visit the Volumes page
    And I clear the search bar
    And I click the button "+"
    Then I expect the "Volume" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I click the "<cloud>" button in the "Select Cloud" dropdown in the "volume" add form
    Then I expect the field "Name" in the volume add form to be visible within max 4 seconds
    When I set the value "<volume-name>" to field "Name" in the "volume" add form
    And I open the "Location" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I click the "<location>" button in the "Location" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I click the button "Add" in the "volume" add form
    And I wait for 5 seconds
    Then "<volume-name>" volume should be present within 30 seconds
    When I wait for 5 seconds
    And I search for "<volume-name>"
    And I wait for 2 seconds
    And I click the "<volume-name>" "volume"
    And I expect the "volume" page to be visible within max 5 seconds
    And I wait for 60 seconds
    Then I click the "Delete" action button in the "volume" page
    And I expect the "Delete volume" dialog to be open within 4 seconds
    And I click the "Delete" button in the "Delete volume" dialog
    When I visit the Home page
    And I wait for 2 seconds
    Then I should see a(n) "request" log entry of action "delete_volume" added "a few seconds ago" in the "dashboard" page within 20 seconds
    When I visit the Volumes page
    And I clear the search bar
    And I search for "<volume-name>"
    Then "<volume-name>" volume should be absent within 30 seconds

    Examples: Providers to be tested
    | cloud         | location       | volume-name                  |
    | Digital Ocean | Amsterdam 3    | mp-test-volume-do-random     |
    | Google Cloud  | europe-west1-c | mp-test-volume-gce-random    |
    | Alibaba Cloud | us-west-1a     | mp-test-volume-aliyun-random |
    | AWS Advantis  | us-west-2a     | mp-test-volume-ec2-random    |

  @mp-test-create-volume-openstack
  Scenario: Create a volume in Openstack provider
    Given "Openstack" cloud has been added
    And I wait for 5 seconds
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
    Then "mp-test-volume-openstack-random" volume should be absent within 30 seconds

  @mp-test-create-volume-arm
  Scenario: Create a volume in Azure ARM provider
    Given "Microsoft Azure" cloud has been added
    And I wait for 40 seconds
    When I visit the Volumes page
    And I clear the search bar
    And I click the button "+"
    Then I expect the "Volume" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I click the "Microsoft Azure" button in the "Select Cloud" dropdown in the "volume" add form
    Then I expect the field "Name" in the volume add form to be visible within max 4 seconds
    When I set the value "mp-test-volume-arm-random" to field "Name" in the "volume" add form
    And I open the "Location" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I click the "East Asia" button in the "Location" dropdown in the "volume" add form
    And I wait for 1 seconds
    And I set the value "armmpdisktestrandom" to field "Resource Group name" in the "volume" add form
    And I click the button "Add" in the "volume" add form
    And I wait for 5 seconds
    Then "mp-test-volume-arm-random" volume should be present within 30 seconds
    When I wait for 5 seconds
    And I click the "mp-test-volume-arm-random" "volume"
    And I expect the "volume" page to be visible within max 5 seconds
    And I wait for 10 seconds
    Then I click the "Delete" action button in the "volume" page
    And I expect the "Delete volume" dialog to be open within 4 seconds
    And I click the "Delete" button in the "Delete volume" dialog
    When I visit the Home page
    And I wait for 2 seconds
    Then I should see a(n) "request" log entry of action "delete_volume" added "a few seconds ago" in the "dashboard" page within 20 seconds
