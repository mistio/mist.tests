@ec2-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @ec2-machine-create
  Scenario Outline: Create a machine in EC2 provider, creating a file using cloud init
    Given "<cloud>" cloud has been added
    When I visit the Home page
    And I wait for the dashboard to load
    When I open the cloud page for "Amazon Web Services"
    Then I expect the "cloud" page to be visible within max 10 seconds
    And I wait for 45 seconds
    And I visit the Images page
    And I wait for 5 seconds
    And I clear the search bar
    And I wait for 5 seconds
    And I search for "ubuntu-focal-20.04"
    Then "ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210223" image should be present within 60 seconds

    When I wait for 60 seconds
    And I visit the Machines page
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
    When I open the "Security group" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "mistio" button in the "Security group" dropdown in the "machine" add form
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
    Then "<machine-name>" machine should be present within 120 seconds
    When I wait for 60 seconds
    And I click the "<machine-name>" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    When I wait for 60 seconds
    And I click the "Shell" action button in the "machine" page
    And I wait for 5 seconds
    Then I expect terminal to open within 30 seconds
    And shell input should be available after 45 seconds
    And I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output

    Examples: Providers to be tested
    | cloud                | size                  | location              | image                                                          | machine-name           |
    | Amazon Web Services  | t2.nano - t2.nano     | ap-northeast-1a       | ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210223 | ec2-mp-test-random     |
