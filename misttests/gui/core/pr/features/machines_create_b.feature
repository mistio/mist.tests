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
    | Rackspace      |  rackspace-ui-test  |
    | Nephoscale     |  nephoscale-ui-test |
    | Softlayer      |  softlayer-ui-test  |
    | Azure          |  azure-ui-test      |

  @machine-destroy
  Scenario Outline: Destroy a machine
    When I wait for the dashboard to load
    When I visit the Machines page
    When I click the "<machine_name>" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds

    Examples: Providers
    |  machine_name       |
    |  rackspace-ui-test  |
    |  nephoscale-ui-test |
    |  softlayer-ui-test  |
    |  azure-ui-test      |
