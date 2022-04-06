@equinix-metal-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  # @equinix_metal-set-private-ipv4
  # Scenario: Create a machine in Equinix Metal provider setting private ipv4
  #   Given "Equinix Metal" cloud has been added
  #   And I wait for 40 seconds
  #   When I visit the Machines page
  #   And I click the button "+"
  #   Then I expect the "Machine" add form to be visible within max 10 seconds
  #   When I open the "Select Cloud" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Equinix Metal" button in the "Select Cloud" dropdown in the "machine" add form
  #   Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
  #   Then I set the value "equinix-metal-mp-test0-random" to field "Machine Name" in the "machine" add form
  #   When I open the "Image" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Ubuntu 18.04 LTS" button in the "Image" dropdown in the "machine" add form
  #   When I open the "Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "c3.small.x86 - 32768 RAM" button in the "Size" dropdown in the "machine" add form
  #   And I open the "Key" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
  #   And I open the "Private IPv4 Subnet Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "/30" button in the "Private IPv4 Subnet Size" dropdown in the "machine" add form
  #   When I open the "Location" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Amsterdam (AM6)" button in the "Location" dropdown in the "machine" add form
  #   Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
  #   When I focus on the button "Launch" in the "machine" add form
  #   And I click the button "Launch" in the "machine" add form
  #   When I visit the Home page
  #   And I visit the Machines page
  #   And I wait for 1 seconds
  #   And I clear the search bar
  #   And I search for "equinix-metal-mp-test0-random"
  #   Then "equinix-metal-mp-test0-random" machine should be present within 60 seconds

  @equinix-metal-machine-create
  Scenario Outline: Create a machine in Equinix Metal provider, creating a file using cloud init
    Given "<cloud>" cloud has been added
    And I wait for 180 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<cloud>" button in the "Select Cloud" dropdown in the "machine" add form
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
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Public IPv4" toggle button in the "machine" add form
    Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine-name>"
    Then "<machine-name>" machine should be present within 120 seconds
    # bare metal could take some minutes...
    And "<machine-name>" machine state has to be "running" within 1800 seconds
    When I wait for 180 seconds
    And I click the "<machine-name>" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    And I expect terminal to open within 7 seconds
    And shell input should be available after 30 seconds
    And I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output

    Examples: Providers to be tested
    | cloud         | size                     | location                 | image            | machine-name                  |
    | Equinix Metal | c3.small.x86 - 32768 RAM | Amsterdam (AM6)          | Ubuntu 18.04 LTS | equinix-metal-mp-test-random  |
