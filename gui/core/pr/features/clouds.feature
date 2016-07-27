@clouds
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load

  @cloud-add
  Scenario Outline:
    When I click the new cloud button
    Then I expect the "Cloud" add form to be visible within max 10 seconds
    And I open the "Choose Provider" drop down
    And I wait for 1 seconds
    When I click the button "<provider>" in the "Choose Provider" dropdown
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my provider "<credentials>" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    Then I click the button "Add Cloud"
    And I click the mist.io button
    Then the "<provider>" provider should be added within 120 seconds

    Examples: Providers
    | provider              | credentials  |
    | Digital Ocean         | DIGITALOCEAN |
    | SoftLayer             | SOFTLAYER    |
    | NephoScale            | NEPHOSCALE   |
    | Rackspace             | RACKSPACE    |
    | Packet                | PACKET       |

    # Added by the Machines feature
#    | AWS                   | AWS          |
    # Added by the Keys feature
    #| Azure                 | AZURE        |
    # Added by the Scripts feature
    #| GCE                   | GCE          |
    # Added by the user actions feature
    #| Linode                | LINODE       |

    # Nope, not really
    #| VMware vCloud         | VMWARE       |
    #| Indonesian Cloud      | INDONESIAN   |
    #| KVM (via libvirt)     | LIBVIRT      |
    #| OpenStack             | OPENSTACK    |
    #| Docker                | DOCKER       |

  @cloud-rename
  Scenario: Cloud Actions
    Given "Digital Ocean" cloud has been added
    Then I open the cloud menu for "Digital Ocean"
    When I rename the cloud "Digital Ocean" to "Renamed"
    Then I close the cloud menu for "Renamed"
    And the "Renamed" provider should be added within 4 seconds

  @cloud-delete
  Scenario: Cloud Actions
    Given "SoftLayer" cloud has been added
    Then I open the cloud menu for "SoftLayer"
    When I delete the "Softlayer" cloud
    Then the "Softlayer" cloud should be deleted
