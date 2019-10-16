@multi
Feature: Multiprovisioning

  Background:
    Given I am logged in to mist

  # TODO: 'GIVEN KEY HAS BEEN ADDED'
  # TODO: Rename scenario names
  @packet
  Scenario: Create a machine, enable monitoring and then destroy it.
    Given "Packet" cloud has been added
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
    And I click the "Key7" button in the "Key" dropdown in the "machine" add form
    And I open the "Private IPv4 Subnet Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "/30" button in the "Private IPv4 Subnet Size" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Amsterdam, NL" button in the "Location" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form


  @mp-test
  Scenario Outline: Create a machine, enable monitoring and then destroy it.
    Given "<provider>" cloud has been added
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<provider>" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "<machine-name>" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<image>" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<size>" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Key7" button in the "Key" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<location>" button in the "Location" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine-name>"
    Then "<machine-name>" machine state has to be "running" within 90 seconds

    Examples: Providers to be tested
    | provider      | size    | location      | image                       | machine-name |
    | Alibaba Cloud  | ecs.n1.tiny (1 cpus/ 1.0Gb RAM )| us-west-1a| ubuntu_18_04_64_20G_alibase_20190624.vhd| aliyun-mp-test-random|
    | EC2           | t2.nano - t2.nano | us-west-2a | Ubuntu Server 16.04 LTS (HVM), SSD Volume Type | ec2-mp-test-random |
    | Digital Ocean | 512mb   | Amsterdam 3   | Debian 10 x64          |    do-mp-test-random |
    | Linode  | Nanode 1GB  | Frankfurt, DE | Ubuntu 19.04    | linode-mp-test-random |
    #| Packet | t1.small.x86 - 8GB RAM | Amsterdam, NL | Ubuntu 19.04 | packet-mp-test1-random | # way too long to see the machine running...
    | GCE    | f1-micro (1 vCPU (shared physical core) and 0.6 GB RAM) | europe-west1-c | ubuntu-1804-bionic-v20191008 | gce-mp-test-random |

  @rackspace
  Scenario: Create a machine, enable monitoring and then destroy it. (way too long...)
    Given "Rackspace" cloud has been added
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
    And I click the "Key7" button in the "Key" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<location>" button in the "Location" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "rackspace-mp-test-random"
    Then "rackspace-mp-test-random" machine state has to be "running" within 180 seconds
    # TODO: separate step
    And I clear the search bar
    And I search for "packet-mp-test0-random"
    Then "packet-mp-test0-random" machine state has to be "running" within 60 seconds

  @azure-arm
  Scenario: Create a machine, enable monitoring and then destroy it. (way too long...)
    Given "Azure ARM" cloud has been added
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Azure ARM" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "arm-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Canonical UbuntuServer 18.04-LTS" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Basic_A0 1 cpus/0.75G RAM/ 20.0GB SSD" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Key7" button in the "Key" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "East Asia" button in the "Location" dropdown in the "machine" add form
    Then I set the value "armmptestrandom" to field "Resource Group name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Storage Account name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Network name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Machine Username" in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "arm-mp-test-random"
    Then "arm-mp-test-random" machine state has to be "running" within 120 seconds
