@multi-provisioning
Feature: Test all possible Images and clouds

  Scenario: Test one provider and one image each time
    Given I am logged in to mist.core
    Then I wait for the links in homepage to appear
    When I visit the Images page
    Then I scroll down until all starred images appear
    When I decide which provider and image I'm going to test
    And I focus on the "MP_MACHINE_TO_TEST" button
    Then I click the image "MP_MACHINE_TO_TEST" of provider "MP_PROVIDER_TO_TEST"
    Then I expect for "single-image-page" page to appear within max 4 seconds
    And I click the button "Create Machine"
    When I type "MP_NEW_MACHINE_NAME" in input with id "create-machine-name"
    And I click the "Select Size" button inside the "Create Machine" panel
    And I click the "MP_MACHINE_SIZE" button inside the "Create Machine" panel
    And I click the "MP_MACHINE_LOCATION_BUTTON" button inside the "Create Machine" panel
    And I click the "MP_MACHINE_LOCATION" button inside the "Create Machine" panel
    And I click the "Select Key" button inside the "Create Machine" panel
    And I click the "mp_key_id_rsa" button inside the "Create Machine" panel
    When I click the "Launch" button inside the "Create Machine" panel
    Then I expect for "create-machine" panel to disappear within max 4 seconds
    Then I click the button "Images"
    And I click the button "Home"
    Then I wait for the links in homepage to appear
    When I visit the Machines page
    And I search for the "MP_NEW_MACHINE_NAME" Machine
    Then I should see the "MP_NEW_MACHINE_NAME" machine added within 20 seconds
    Then I expect for "single-machine-page" page to appear within max 5 seconds
    Then I enable monitoring if it's not enabled
    And I wait for the graphs to appear
    When I focus on the "cpu" graph
    When I focus on the "Add Graph" button
    And I click the button "Add Graph"
    Then I expect for "metric-add-popup" popup to appear within max 30 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the "Select Metric" popup
    Then "entropy" graph should be added within 30 seconds
    When I focus on the "entropy" graph
    Then "entropy" graph should have value > 0 within 400 seconds
    And I delete the "entropy" graph
    And I wait for 3 seconds
    And I click the button "Machines"
    When I click the button "MP_NEW_MACHINE_NAME"
    Then I expect for "single-machine-page" page to appear within max 5 seconds
    When I click the button "Actions"
    Then I expect for "machine-power-popup-popup" popup to appear within max 4 seconds
    When I click the button "Destroy"
    Then I expect for "machine-power-popup-popup" popup to disappear within max 4 seconds
    Then I expect for "dialog-popup" popup to appear within max 4 seconds
    Then I expect for buttons inside "dialog-popup" to be clickable within max 8 seconds
    And  I click the button "Yes"
    Then I expect for "dialog-popup" popup to disappear within max 4 seconds
    And I wait for max 90 seconds for "MP_NEW_MACHINE_NAME" machine from "MP_PROVIDER_TO_TEST" to disappear
    Then I wait for 5 seconds
    And I add the machine to the db as successfuly tested
