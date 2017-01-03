@monitoring
Feature: Create Machine and test monitoring


  Scenario: Create Machine,deploy monitoring agent and check the graphs
    Given I am logged in to mist.core
    # provider docker?
    Given "Docker" cloud has been added

    # create machine
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Choose Cloud" drop down
    And I wait for 1 seconds
    When I click the button "Docker" in the "Choose Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "docker-ui-test" machine
    # enable monitoring
    Then I click the "Launch" button
    And I wait for 3 seconds
    Then I visit the Machines page
    Then "docker-ui-test" machine state has to be "running" within 30 seconds


    When I click the "docker-ui-test" "machine"

#    And I expect for "dialog-popup" modal to appear within max 400 seconds
#    And I click the "_x_" button inside the "Success" modal
#    When I focus on the "third" button
#    And I click the button "third"
#    Then I expect for "single-machine-page" page to appear within max 4 seconds
#    And I wait for the graphs to appear
#
#    # disable monitoring and wait for success message
#    When I focus on the "Disable" button
#    And I click the button "Disable"
#    And I expect for "dialog-popup" modal to appear within max 4 seconds
#    And I click the "Yes" button inside the "Disable monitoring" modal
#    And I expect for "dialog-popup" modal to appear within max 60 seconds
#    And I click the "_x_" button inside the "Success" modal
#
#    # Go to machines page and destroy the machine
#    When I focus on the "Machines" button
#    And I click the button "Machines"
#    Then I wait for "Machines" list page to load
#    When I clear the machines search bar
#    Then I search for the "third" Machine
#    And I wait for 1 seconds
#    When I choose the "third" machine
#    And I click the button "Actions"
#    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
#    When I click the "Destroy" button inside the "Actions" popup
#    Then I expect for "dialog-popup" modal to appear within max 4 seconds
#    When I click the button "Yes"
#    And "third" machine state should be "terminated" within 200 seconds
#
#    Then I logout
