@monitoring
Feature: Create Machine and test monitoring


  @enable-monitoring
  Scenario: Create Machine,deploy monitoring agent and check the graphs
    Given I am logged in to mist.core
    When I wait for the dashboard to load
    Given "Docker" cloud has been added
    Given "Testkey" key has been added
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
    # launch button
    Then I click the "Launch" button
    And I wait for 3 seconds
    Then I visit the Machines page
    Then "docker-ui-test" machine state has to be "running" within 30 seconds
    When I click the "docker-ui-test" "machine"
    # check that graphs have appeared


  @add-custom-graph




  @add-rule


  @disable-monitoring


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

