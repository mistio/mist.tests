@multiprovisioning-2
Feature: Multiprovisioning

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear

  @packet-set-private-ipv4
  Scenario: Create a machine in Packet provider setting private ipv4
    Given "Packet" cloud has been added
    And key "Key-random" has been added via API request
    And I wait for 40 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Packet" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "packet-mp-test0-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Ubuntu 19.04" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "t1.small.x86 - 8GB RAM" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Key-random" button in the "Key" dropdown in the "machine" add form
    And I open the "Private IPv4 Subnet Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "/30" button in the "Private IPv4 Subnet Size" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Amsterdam, NL" button in the "Location" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "packet-mp-test0-random"
    Then "packet-mp-test0-random" machine should be present within 60 seconds

# TODO: when cloud_init in Aliyun/Linode is fixed, move to mp-test-with-cloud-init
  @mp-test-without-cloud-init
  Scenario Outline: Create a machine in various providers, without cloud init
    Given "<provider>" cloud has been added
    And I wait for 40 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<provider>" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "<machine-name>" to field "Machine Name" in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<location>" button in the "Location" dropdown in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<image>" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<size>" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Key-random" button in the "Key" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine-name>"
    Then "<machine-name>" machine should be present within 60 seconds

    Examples: Providers to be tested
    | provider      | size                              | location       | image                                    | machine-name          |
    | Alibaba Cloud | ecs.xn4.small (1 cpus/ 1.0Gb RAM )| us-west-1a     | ubuntu_18_04_64_20G_alibase_20190624.vhd | aliyun-mp-test-random |
    | Linode        | Nanode 1GB                        | Frankfurt, DE  | Ubuntu 19.04                             | linode-mp-test-random |

  @rackspace
  Scenario: Create a machine in Rackspace provider
    Given "Rackspace" cloud has been added
    And I wait for 40 seconds
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
    And I click the "Ubuntu 18.04 LTS (Bionic Beaver) (PVHVM)" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "512MB Standard Instance" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Key-random" button in the "Key" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "rackspace-mp-test-random"
    Then "rackspace-mp-test-random" machine should be present within 60 seconds
