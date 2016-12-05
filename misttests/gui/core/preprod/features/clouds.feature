@clouds
Feature: Add second-tier clouds

  Scenario Outline: Add <provider> and create/reboot/destroy a Ubuntu 15.04 instance on it
    Given I am logged in to mist.core
    And "<provider>" cloud has been added
#    When I ensure "<provider>" cloud is enabled
#    And I visit the Machines page
#    When I click the button "Create Machine"
#    Then I expect for "create-machine" panel to appear within max 4 seconds
#    When I fill in a "staging_<provider>_random" machine name
#    And I click the "Select Provider" button inside the "Create Machine" panel
#    And I click the "<provider>" button inside the "Create Machine" panel
#    And I click the "Select Image" button inside the "Create Machine" panel
#    And I click the "<image_name>" button inside the "Create Machine" panel
#    And I click the "Select Size" button inside the "Create Machine" panel
#    And I click the "<size>" button inside the "Create Machine" panel
#    And I click the "Select Location" button inside the "Create Machine" panel
#    And I click the "<location>" button inside the "Create Machine" panel
#    And I click the "Select Key" button inside the "Create Machine" panel
#    And I add new machine key with name "staging_<provider>_random_key" or I select it
#    And I click the button "Enable Monitoring"
#    When I click the "Launch" button inside the "Create Machine" panel
#    Then I expect for "create-machine" panel to disappear within max 4 seconds
#    And I search for the "staging_<provider>_random" Machine
#    Then I should see the "staging_<provider>_random" machine added within 30 seconds
#    And "staging_<provider>_random" machine state should be "running" within 400 seconds

#    When I choose the "randomly_created" machine
#    And I click the button "Actions"
#    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
#    When I click the "Reboot" button inside the "Actions" popup
#    Then I expect for "dialog-popup" popup to appear within max 4 seconds
#    When I click the button "Yes"
#    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
#    And "randomly_created" machine state should be "running" within 200 seconds
#
#    When I click the button "Actions"
#    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
#    When I click the button "Destroy"
#    Then I expect for "dialog-popup" popup to appear within max 4 seconds
#    When I click the button "Yes"
#    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
#    Then "randomly_created" machine state should be "terminated" within 200 seconds

    Examples: Providers
    | provider              | size                    | location        | image_name                     |
#    | Azure                 | ExtraSmall              | East US         | Ubuntu Server 15.04 DAILY      |
#    | DigitalOcean          | 512mb                   | New York 1      | Ubuntu 15.04 x64               |
#    | GCE                   | f1-micro                | asia-east1-b    | ubuntu-1504-vivid-v20151120    |
#    | Linode                | Linode 1024             | Dallas          | Ububntu 15.04                  |
#    | NephoScale            | CS05                    | SJC-1           | Ubuntu Server 14.04 LTS 64-bit |
#    | Rackspace             | 512mb Standard Instance | ?               | Ubuntu 15.10                   |
#    | SoftLayer             | 1CPU, 1gb ram           | Amsterdam       | Ubuntu - Latest (64 bit)       |
#    | EC2                   | Micro Instance          | ap-northeast-1c | Ubuntu Server 14.04. LTS       |
#    | VMware vCloud         | ?                       | ?               | ?                              |
#    | Packet.net            | ?                       | ?               | Ubuntu 14.04 LTS               |
    | KVM (via libvirt)      | ?                       | ?               | ?                              |
#    | Indonesian Cloud      | INDONESIAN   |
#    | OpenStack             | OPENSTACK    |
#    | Docker                | DOCKER       |