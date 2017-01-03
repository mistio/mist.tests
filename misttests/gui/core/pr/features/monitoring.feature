@monitoring
Feature: Create Machine and test monitoring


  Scenario: Create Machine,deploy monitoring agent and check the graphs
    Given I am logged in to mist.core
    # provider docker?
    Given "EC2" cloud has been added






    And I click the button "Create Machine"
    When I fill in a "random third" machine name
    And I click the "Select Size" button inside the "Create Machine" panel
    And I click the "Micro Instance" button inside the "Create Machine" panel
    And I click the "Select Location" button inside the "Create Machine" panel
    And I click the "ap-northeast-1a" button inside the "Create Machine" panel
    And I click the "Select Key" button inside the "Create Machine" panel
    And I click the "Add Key" button inside the "Create Machine" panel
    Then I expect for "key-add-popup" popup to appear within max 4 seconds
    When I fill "third_machine_key" as key name
    And I click the "Generate" button inside the "Add key" popup
    Then I expect for "key-generate-loader" loader to finish within max 10 seconds
    When I click the "Add" button inside the "Add key" popup
    Then I expect for "key-add-popup" popup to disappear within max 4 seconds
    When I click the "Launch" button inside the "Create Machine" panel
    Then I expect for "create-machine" panel to disappear within max 4 seconds
    When I click the button "Images"
    Then I expect for "image-list-page" page to appear within max 4 seconds
    When I click the button "Home"
    Then I expect for "home-page" page to appear within max 4 seconds
    When I visit the Machines page after the counter has loaded
    And I search for the "third" Machine
    Then I should see the "third" machine added within 60 seconds
#
#    # wait for machine state to become running
#    Then "third" machine state should be "running" within 120 seconds
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
