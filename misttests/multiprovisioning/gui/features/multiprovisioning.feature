@multi-provisioning
Feature: Multiprovisioning testing against prod. Make sure that create machine and enabling monitoring works fine across multiple providers

  Background:
    Given I am logged in to mist.core

  @machine-create
  Scenario: Create a machine in Docker provider
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    And I click the button "<provider>" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "ui-test-create-machine-random" machine
    And I wait for 3 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I click the "Launch" button with id "appformsubmit"
    When I visit the Home page
    And I visit the Machines page
    And I search for "ui-test-create-machine-random"
    Then "ui-test-create-machine-random" machine state has to be "running" within 60 seconds


  #  Examples: Image according to provider
  #  | provider        | field       | script                                                                      | name    | type       |
  #  | GCE        | Script      | #!/bin/bash\necho bla > ~/kati                                              | Script1 | Executable |
  #  | AWS        | Github Repo | https://github.com/ansible/ansible-examples                                 | Script2 | Executable |
  #  | Digital Ocean           | Url         | https://github.com/ansible/ansible-examples/blob/master/lamp_simple/site.yml| Script3 | Executable |
