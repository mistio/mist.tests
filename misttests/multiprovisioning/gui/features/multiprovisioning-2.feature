@multiprovisioning-2
Feature: Multiprovisioning

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear

  @add-Key
  Scenario: Add key needed for tests
    Given key "Keyrandom" has been generated and added via API request
    # TODO: Add openstack cloud here to make sure that networks are 
    # visible in create machine form. Change this when
    # https://gitlab.ops.mist.io/mistio/mist.api/issues/39 is resolved
    #Given "Openstack" cloud has been added

  @rackspace-set-expiration-date
  Scenario: Create a machine in Rackspace provider, setting expiration date
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
    And I wait for 1 seconds
    And I click the "Set Expiration" toggle button in the "machine" add form
    And I wait for 1 seconds
    And I set an expiration in "12" "minutes" with a notify of "1" "minutes" before
    And I wait for 1 seconds
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "rackspace-mp-test-random"
    Then "rackspace-mp-test-random" machine should be present within 60 seconds

  @azure-arm-cloud-init
  Scenario: Create a machine in Azure arm provider with new resource group, storage account, network and cloud init
    Given "Azure ARM" cloud has been added
    And I wait for 40 seconds
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
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "East Asia" button in the "Location" dropdown in the "machine" add form
    Then I set the value "armmptestrandom" to field "Resource Group name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Storage Account name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Network name" in the "machine" add form
    Then I set the value "armmptestrandom" to field "Machine Username" in the "machine" add form
    Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "arm-mp-test-random"
    Then "arm-mp-test-random" machine should be present within 60 seconds

  # @aliyun-cloud-init
  # Scenario: Create a machine in aliyun provider, creating a file using cloud init
  #   Given "Alibaba Cloud" cloud has been added
  #   And I wait for 40 seconds
  #   When I visit the Machines page
  #   And I click the button "+"
  #   Then I expect the "Machine" add form to be visible within max 10 seconds
  #   When I open the "Select Cloud" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Alibaba Cloud" button in the "Select Cloud" dropdown in the "machine" add form
  #   Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
  #   Then I set the value "aliyun-mp-test-random" to field "Machine Name" in the "machine" add form
  #   When I open the "Location" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "us-west-1a" button in the "Location" dropdown in the "machine" add form
  #   When I open the "Image" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "ubuntu_18_04_64_20G_alibase_20190624.vhd" button in the "Image" dropdown in the "machine" add form
  #   When I open the "Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "ecs.n1.tiny (1 cpus/ 1.0Gb RAM )" button in the "Size" dropdown in the "machine" add form
  #   And I open the "Key" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
  #   Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
  #   When I focus on the button "Launch" in the "machine" add form
  #   And I click the button "Launch" in the "machine" add form
  #   When I visit the Home page
  #   And I visit the Machines page
  #   And I wait for 1 seconds
  #   And I clear the search bar
  #   And I search for "aliyun-mp-test-random"
  #   Then "aliyun-mp-test-random" machine should be present within 60 seconds

  @linode-post-deploy-script
  Scenario: Create a machine in linode, setting post-deploy script
    Given "Linode" cloud has been added
    And I wait for 40 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Linode" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "linode-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Frankfurt, DE" button in the "Location" dropdown in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Ubuntu 19.04" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Nanode 1GB" button in the "Size" dropdown in the "machine" add form
    And I click the "Run post-deploy script" toggle button in the "machine" add form
    And I wait for 1 seconds
    Then I set the "Inline script" script "#!/bin/bash\ntouch ~/new_file"
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "linode-mp-test-random"
    Then "linode-mp-test-random" machine should be present within 60 seconds

  # @openstack
  # Scenario: Create a machine in Openstack provider, with floating ip
  #   When I visit the Machines page
  #   And I click the button "+"
  #   Then I expect the "Machine" add form to be visible within max 10 seconds
  #   When I open the "Select Cloud" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Openstack" button in the "Select Cloud" dropdown in the "machine" add form
  #   Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
  #   Then I set the value "openstack-mp-test-random" to field "Machine Name" in the "machine" add form
  #   When I open the "Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "m1.tiny" button in the "Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   Then I set the value "private" to field "Networks" in the "machine" add form
  #   And I open the "Key" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
  #   Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
  #   When I focus on the button "Launch" in the "machine" add form
  #   And I click the button "Launch" in the "machine" add form
  #   When I visit the Home page
  #   And I visit the Machines page
  #   And I wait for 1 seconds
  #   And I clear the search bar
  #   And I search for "openstack-mp-test-random"
  #   Then "openstack-mp-test-random" machine should be present within 60 seconds

  @verify-scripts
  Scenario Outline: Verify that file created with cloud-init/post-deploy exists
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine>"
    Then "<machine>" machine state has to be "running" within 60 seconds
    And I click the "<machine>" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Shell" action button in the "machine" page
    And I expect terminal to open within 3 seconds
    And shell input should be available after 30 seconds
    And I type in the terminal "sudo su"
    And I wait for 1 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output
    And I close the terminal

  Examples: Providers to be tested
    | machine                |
   # | aliyun-mp-test-random  |
    | arm-mp-test-random     |
    | linode-mp-test-random  |


  @verify-expiration
  Scenario: Verify that a reminder email will be received and machine will be stopped
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Machine is about to expire" within 660 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "rackspace-mp-test-random"
    Then "rackspace-mp-test-random" machine state has to be "stopped" within 240 seconds

# TODO: 300