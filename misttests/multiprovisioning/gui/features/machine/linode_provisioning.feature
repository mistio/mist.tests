@linode-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @linode-machine-create
  Scenario: Create a machine in linode, setting post-deploy script
    Given "Linode" cloud has been added
    And I wait for 180 seconds
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
    And I click the "eu-central" button in the "Location" dropdown in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Ubuntu 20.04 LTS" button in the "Image" dropdown in the "machine" add form
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
    Then "linode-mp-test-random" machine should be present within 120 seconds
    When I wait for 60 seconds
    And I click the "linode-mp-test-random" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    When I wait for 90 seconds
    And I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    Then I expect terminal to open within 7 seconds
    And shell input should be available after 30 seconds
    When I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output
