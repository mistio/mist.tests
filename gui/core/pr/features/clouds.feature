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
    When I use my provider "<credentials>" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    Then I click the button "Add Cloud"
    And I visit the Home page
    And I scroll the clouds list into view
    Then the "<provider>" provider should be added within 120 seconds

    Examples: Providers
    | provider              | credentials  |
    | Azure                 | AZURE        |
    | Digital Ocean         | DIGITALOCEAN |
    | SoftLayer             | SOFTLAYER    |
    | NephoScale            | NEPHOSCALE   |
    | Rackspace             | RACKSPACE    |
    | Packet                | PACKET       |
    | GCE                   | GCE          |
    | Linode                | LINODE       |
    | AWS                   | AWS          |

    # Nope, not really
    #| VMware vCloud         | VMWARE       |
    #| Indonesian Cloud      | INDONESIAN   |
    #| KVM (via libvirt)     | LIBVIRT      |
    #| OpenStack             | OPENSTACK    |
    #| Docker                | DOCKER       |

  @cloud-rename
  Scenario: Cloud Actions
    Given "Azure" cloud has been added
    Then I open the cloud menu for "Azure"
    When I rename the cloud "Azure" to "Renamed"
    Then I close the cloud menu for "Renamed"
    And I refresh the page
    Then I wait for the dashboard to load
    And the "Renamed" provider should be added within 4 seconds

  @cloud-delete
  Scenario: Cloud Actions
    Given "SoftLayer" cloud has been added
    Then I open the cloud menu for "SoftLayer"
    When I delete the "Softlayer" cloud
    Then the "Softlayer" cloud should be deleted within "8" seconds
