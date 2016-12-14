# Created by spiros at 7/12/2016
Feature: Machine actions for polymer

  Background:
    Given I am logged in to mist.core
    And I am in the new UI

  @machine-create
  Scenario Outline: Create a machine
    When I wait for the dashboard to load
    Given "<provider>" cloud has been added
    Given "Testkey" key has been added
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    When I click the button "<provider>" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "<provider>" to create the "<machine_name>" machine
    Then I click the "Launch" button
    And I wait for 3 seconds
    Then I visit the Machines page
    Then "<machine_name>" machine should be present within 40 seconds
    Then I visit the Home page

    Examples: Providers
    | provider       |  machine_name       |
    | Docker         |  docker-ui-test     |
#    | AWS            |  aws-ui-test        |
#    | Digital Ocean  |  do-ui-test         |
#    | Packet         |  packet-ui-test     |
#    | Openstack      |  openstack-ui-test  |

  @machine-destroy
  Scenario Outline: Destroy a machine
    When I wait for the dashboard to load
    When I visit the Machines page
    And I wait for 2 seconds
    When I click the "<machine_name>" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    Then I click the button "Destroy" from the menu of the "machine" edit form
    And I expect the dialog "Destroy 1 Machine" is open within 4 seconds
    And I wait for 2 seconds
    And I click the "Destroy" button in the dialog "Destroy 1 Machine"
    And I expect the dialog "Destroy 1 Machine" is closed within 4 seconds

    Examples: Providers
    |  machine_name       |
    |  Docker-ui-test-2   |
#    |  aws-ui-test        |
#    |  do-ui-test         |
#    |  packet-ui-test     |
#    |  openstack-ui-test  |
