@digital-ocean-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @digital-ocean-machine-create
  Scenario Outline: Create a machine in digital ocean provider, creating a file using cloud init and enabling monitoring
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
    Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
    And I wait for 1 seconds
    And I click the "Enable monitoring" toggle button in the "machine" add form
    And I wait for 1 seconds
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine-name>"
    Then "<machine-name>" machine should be present within 120 seconds
    When I wait for 60 seconds
    And I click the "<machine-name>" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 120 seconds
    Then I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    And I expect terminal to open within 7 seconds
    And shell input should be available after 30 seconds
    And I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output
    And I close the terminal
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine-name>"
    Then "<machine-name>" machine state has to be "running" within 30 seconds
    And I click the "<machine-name>" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
    Then 5 graphs should be visible within max 30 seconds in the "machine" page
    When I visit the Home page
    And I wait for the navigation menu to appear
    Then I wait for the monitoring graphs to appear in the "dashboard" page


  Examples: Providers to be tested
    | cloud        | size                                      | location         | image                                        | machine-name           |
    | DigitalOcean | 1 CPU, 0.5 GB, 20 GB SSD Disk, $6.0/month | Amsterdam 3      | Ubuntu 18.04 (LTS) x64                       | do-mp-test-random      |
