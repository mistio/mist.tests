@gce-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @gce-machine-create
  Scenario Outline: Create a machine in GCE provider, creating a file using cloud init
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
    And I click the button that contains "<image>" in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<size>" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "<machine-name>"
    Then "<machine-name>" machine should be present within 180 seconds
    And "<machine-name>" machine state has to be "running" within 180 seconds
    And I click the "<machine-name>" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 60 seconds
    Then I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    And I expect terminal to open within 5 seconds
    And shell input should be available after 30 seconds
    And I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output

    Examples: Providers to be tested
    | cloud         | size                                                    | location         | image                         | machine-name           |
    | Google Cloud  | f1-micro (1 vCPU (shared physical core) and 0.6 GB RAM) | europe-west1-c   | ubuntu-1804-bionic            | gce-mp-test-random     |
