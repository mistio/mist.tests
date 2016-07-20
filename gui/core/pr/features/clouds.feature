@clouds
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    Then I wait for the links in homepage to appear
    Then I expect for "addBtn" to be clickable within max 20 seconds

  @cloud-add
  Scenario Outline:
    When I click the button by "addBtn" id_name
    Then I expect the page Clouds to be visible within max 10 seconds
    And I open the "Choose Provider" drop down
    And I wait for 1 seconds
    When I click the button "<provider>" in the "Choose Provider" dropdown
    Then I expect the label "Title *" to be visible within max 4 seconds
    When I use my provider "<credentials>" credentials
    And I click the button "Add Cloud"
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
    Given "Digital Ocean" cloud has been added
    When I rename the cloud "Digital Ocean" to "Renamed"
    Then the "Renamed" provider should be added within 4 seconds

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