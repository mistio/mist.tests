@monitoring
Feature: Monitoring

  # FIXME: When #1363 is resolved, enable monitoring when creating machine
  @enable-monitoring
  Scenario: Enable monitoring when creating machine and check the graphs
    Given I am logged in to mist.core
    And cloud "Docker" has been added via API request
    And I have given card details if needed
    And key "Key1" has been added via API request
    When I visit the Machines page
    And I wait for 1 seconds
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 5 seconds
    When I open the "Select Cloud" drop down
    And I wait for 1 seconds
    And I click the button "Docker" in the "Select Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "monitored-machine-random" to field "Machine Name" in "machine" add form
    When I open the "Image" drop down
    And I click the button "mist/ubuntu-14.04:collectd" in the "Image" dropdown
    When I open the "Key" drop down
    And I click the button "Key1" in the "Key" dropdown
    And I wait for 1 seconds
    #And I click the "Enable monitoring" button with id "app-form-createForm-monitoring"
    #And I wait for 1 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I wait for 2 seconds
    And I click the "Launch" button with id "appformsubmit"
    #And I wait for 10 seconds
    And I wait for 2 seconds
    And I visit the Home page
    And I visit the Machines page
    And I search for "monitored-machine-random"
    Then "monitored-machine-random" machine state has to be "running" within 30 seconds
    When I click the "monitored-machine-random" "machine"
    #And I wait for 15 seconds
    #Then I wait for the graphs to appear
    #And 9 graphs should be visible within max 30 seconds
    And I wait for 2 seconds
    And I click the button "Enable Monitoring"
    And I wait for 5 seconds
    Then I wait for the graphs to appear
    And 9 graphs should be visible within max 30 seconds
    #And I wait for 10 seconds

  @add-entropy-graph
  Scenario: Add custom graph and make sure an extra graph is visible
    When I scroll to the bottom of the page
    And I click the button "Add Graph"
    Then I expect for "selectTarget" modal to appear within max 20 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "kernel" button inside the popup with id "selectTarget"
    And I click the "kernel.entropy_avail" button inside the popup with id "selectTarget"
    Then "kernel entropy_avail" graph should appear within 30 seconds
    And 10 graphs should be visible within max 20 seconds

  @monitoring-home-page
  Scenario: Visit Home page and verify that polyana-dashboard is there
    When I visit the Home page
    And I wait for the links in homepage to appear
    Then I wait for the graphs to appear
    And "Load on all monitored machines" graph should have some values

  @disable-monitoring
  Scenario: Disable monitoring
    When I visit the Machines page
    And I click the "monitored-machine-random" "machine"
    And I wait for 2 seconds
    And I click the "Disable Monitoring" button with id "monitoring-menu-wrapper"
    And I wait for 2 seconds
    And I click the "Disable Monitoring" button with id "monitoring-menu-wrapper"
    Then I expect the dialog "Disable Machine Monitoring" is open within 5 seconds
    When I click the "Disable Monitoring" button in the dialog "Disable Machine Monitoring"
    Then I expect the dialog "Disable Machine Monitoring" is closed within 5 seconds
    And graphs should disappear within 15 seconds
