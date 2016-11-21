@machines
Feature: Machines

  Background:
    Given I am logged in to mist.core


  @machine-probing
  Scenario: Machine probing
    When I visit the Machines page after the counter has loaded
    And I click the button "sshtesting"
    Then I expect for "single-machine-page" page to appear within max 4 seconds
    Given ssh key with name "TESTING_MACHINE" is added
    Then I click the button "Probe"
    And I wait for probing to finish for 100 seconds max
    And probing was successful


  @machine-ssh
  Scenario: Connect with ssh
    When I visit the Machines page after the counter has loaded
    And I click the button "sshtesting"
    Then I expect for "single-machine-page" page to appear within max 4 seconds
    Given ssh key with name "TESTING_MACHINE" is added
    Then I click the button "Shell"
    And I test the ssh connection
    And I wait for 1 seconds


   @machine-rule
   Scenario: Add rule
    When I visit the Machines page after the counter has loaded
    And I click the button "mytestmonitor2"
    Then I expect for "single-machine-page" page to appear within max 5 seconds
    And I wait for the graphs to appear
    When I focus on the "Add Graph" button
    And I remove previous rules
    When I focus on the "Add Rule" button
    And I click the button "Add Rule"
    Then I expect for "basic-condition" to be visible within max 20 seconds
    When I click the button "Load"
    And I click the button "CPU"
    And I fill "2" as rule value
    And I click the button ">"
    And I click the button "<"
    And I click the button "alert"
    And I click the button "REBOOT"
    When I focus on the "cpu" graph
    Then there should be a gap in the "cpu" graph within 200 seconds
    When I remove previous rules
    And I wait for 3 seconds


  @machine-graph
  Scenario: Add graph
    When I visit the Machines page after the counter has loaded
    And I click the button "mytestmonitor2"
    Then I expect for "single-machine-page" page to appear within max 5 seconds
#    Given ssh key with name "MYTESTMONITOR" is added
#    When I focus on the "Machines" button
#    Then I enable monitoring if it's not enabled
    And I wait for the graphs to appear
    When I focus on the "cpu" graph
    When I focus on the "Add Graph" button
    And I click the button "Add Graph"
    Then I expect for "metric-add-popup" popup to appear within max 30 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the "Select Metric" popup
    Then "entropy" graph should be added within 30 seconds
    When I focus on the "entropy" graph
    Then "entropy" graph should have value > 0 within 30 seconds
    And I delete the "entropy" graph
    And I wait for 3 seconds


  @machine-custom-graph
  Scenario: Add custom graph
    When I visit the Machines page after the counter has loaded
    And I click the button "mytestmonitor2"
    Then I expect for "single-machine-page" page to appear within max 5 seconds
    And I wait for the graphs to appear
    When I focus on the "Add Graph" button
    And I click the button "Add Graph"
    Then I expect for "metric-add-popup" popup to appear within max 30 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the button "CUSTOM"
    Then I expect for "metric-add-custom-popup" popup to appear within max 5 seconds
    When I give a "my_metric" name for my custom metric
    And I give a default script for python script
    And I click the button "Deploy"
    Then "my_metric" graph should be added within 60 seconds
    When I focus on the "my_metric" graph
    Then "my_metric" graph should have value > 0 within 100 seconds
    And I delete the "my_metric" graph
    And I wait for 3 seconds
