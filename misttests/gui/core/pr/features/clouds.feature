@clouds
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load

  @cloud-add
  Scenario Outline:
    When I click the new cloud button
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    And I open the "Choose Provider" drop down
    And I wait for 1 seconds
    When I click the button "<provider>" in the "Choose Provider" dropdown
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "<provider>" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    Then I click the button "Add Cloud" in "cloud" add form
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "<provider>" provider should be added within 120 seconds

    Examples: Providers
    | provider       |
    | Azure          |
    | Digital Ocean  |
    | SoftLayer      |
    | NephoScale     |
    | Rackspace      |
    | Packet         |
    | GCE            |
    | Linode         |
    | AWS            |
    | Docker         |
    | Openstack      |
    | Vultr          |
    | Azure ARM      |
    | Vmware         |
    | Indonesian     |
    | KVM (Via Libvirt)           |
#    | Other Server   |
#    | HostVirtual    |

  @cloud-rename
  Scenario: Rename a cloud
    Given "Openstack" cloud has been added
    Then I open the cloud menu for "Openstack"
    When I rename the cloud "Openstack" to "Renamed"
    And I click the "save title" button
    And I wait for 3 seconds
    #When I click the mist-logo
    When I visit mist_url
    And I wait for the dashboard to load
    Then "Renamed" cloud has been added


  @cloud-delete
  Scenario: Delete a cloud
    Given "Renamed" cloud has been added
    Then I open the cloud menu for "Renamed"
    And I click the "delete cloud" button
    And I wait for 2 seconds
    Then the "Renamed" cloud should be deleted
