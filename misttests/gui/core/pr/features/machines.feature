# Created by spiros at 7/12/2016
Feature: Machine actions for polymer

  Background:
    Given I am logged in to mist.core
    And I am in the new UI


  @machine-create
  Scenario Outline: Create a machine
    When I wait for the dashboard to load
    Given "<provider>" cloud has been added
    # given key has been added...
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    When I click the button "<provider>" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "<provider>" in the machine "add" form


    Examples: Providers
    | provider       |
    | AWS            |

