@clouds
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    Given the Images counter has loaded

  @cloud-add
  Scenario Outline:
    When I click the button by "addBtn" id_name
    Then I expect for "cloud-add" element to be visible within max 10 seconds
    And I open the Provider drop down
    And I wait for 1 seconds
    When I click the provider button <provider>
    Then I expect for "Title *" label to be visible within max 4 seconds
    When I use my provider "<credentials>" credentials
    And I click the Add provider button
    And I wait for 2 seconds
    And I refresh the page
    Then the "<provider>" provider should be added within 120 seconds

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
    Then the "GCE" cloud should be deleted