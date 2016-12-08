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
#    Then I visit the keys page
#    When I click the button "+"
#    Then I expect the "Key" add form to be visible within max 10 seconds
#    When I set the value "TestKey" to field "Name" in "key" add form
#    Then I click the button "Generate" in "key" add form
#    And I wait for 5 seconds
#    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
#    When I focus on the button "Add" in "key" add form
#    And I click the button "Add" in "key" add form
#    Then I expect the "key" edit form to be visible within max 5 seconds
#    When I visit the Home page
#    When I wait for the dashboard to load
#    When I visit the Keys page
#    Then "TestKey" key should be present within 15 seconds
    ########################################################
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

