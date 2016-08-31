@clouds
Feature: Add second-tier clouds

  Background:
    Given I am logged in to mist.core

  @cloud-add
  Scenario Outline:
    When I click the button "Add cloud"
    Then I expect for "new-cloud-provider" panel to appear within max 4 seconds
    And I click the button "<provider>"
    And I expect for "new-cloud-provider" panel to disappear within max 4 seconds
    Then I expect for "cloud-add-fields" to be visible within max 4 seconds
    And I wait for 1 seconds
    When I use my "<credentials>" credentials
    And I click the button "Add"
    Then the "<provider>" cloud should be added within 120 seconds

    
    Examples: Providers
    | provider              | credentials  |
    | DigitalOcean          | DIGITALOCEAN |
    | SoftLayer             | SOFTLAYER    |
    | NephoScale            | NEPHOSCALE   |
    | Rackspace             | RACKSPACE    |
    | Packet.net            | PACKET       |

    # Added by the Machines feature
    #| EC2                   | EC2          |
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
    Given "DigitalOcean" cloud has been added
    When I click the button "DigitalOcean"
    Then I expect for "cloud-edit-popup" popup to appear within max 4 seconds
    When I rename the cloud to "Renamed"
    And I click the "OK" button inside the "Edit cloud" popup
    When I click the "_x_" button inside the "Edit cloud" popup
    Then I expect for "cloud-edit-popup" popup to disappear within max 4 seconds
    And the "Renamed" cloud should be added within 4 seconds

  @cloud-delete
  Scenario: Cloud Actions
    Given "SoftLayer" cloud has been added
    When I click the button "SoftLayer"
    Then I expect for "cloud-edit-popup" popup to appear within max 4 seconds
    When I click the "Delete" button inside the "Edit cloud" popup
    And I wait for 1 seconds
    And I click the "Yes" button inside the "Edit cloud" popup
    Then I expect for "cloud-edit-popup" popup to disappear within max 8 seconds
    Then the "SoftLayer" cloud should be deleted
