@monitoring
Feature: Monitoring

  # FIXME: When #1363 is resolved, enable monitoring when creating machine
  @enable-monitoring
  Scenario: Enable monitoring when creating machine and check the graphs
    Given I am logged in to mist
    And cloud "Docker" has been added via API request
    And I have given card details if needed
    And key "Key1" has been added via API request
    When I visit the Machines page
    And I wait for 1 seconds
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 5 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Docker" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "monitored-machine-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I click the "Ubuntu 14.04 - mist.io image" button in the "Image" dropdown in the "machine" add form
    When I open the "Key" dropdown in the "machine" add form
    And I click the "Key1" button in the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    #And I click the "Enable monitoring" button with id "app-form-createForm-monitoring"
    #And I wait for 1 seconds
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I wait for 2 seconds
    And I click the button "Launch" in the "machine" add form
    #And I wait for 10 seconds
    And I wait for 2 seconds
    And I visit the Home page
    And I visit the Machines page
    And I search for "monitored-machine-random"
    Then "monitored-machine-random" machine state has to be "running" within 100 seconds
    When I click the "monitored-machine-random" "machine"
    #And I wait for 15 seconds
    #Then I wait for the graphs to appear
    #And 9 graphs should be visible within max 30 seconds
    And I wait for 2 seconds
    And I click the button "Enable Monitoring" in the "machine" page
    And I wait for 5 seconds
    Then I wait for the monitoring graphs to appear in the "machine" page
    And 9 graphs should be visible within max 30 seconds in the "machine" page
    #And I wait for 10 seconds

  @add-entropy-graph
  Scenario: Add custom graph and make sure an extra graph is visible
    When I scroll to the bottom of the page
    And I click the button "Add Graph" in the "machine" page
    Then I expect the "Select target for graph" dialog to be open within 10 seconds
    And I expect the metric buttons to appear within 30 seconds
    And I click the "kernel" button in the "Select target for graph" dialog
    And I click the "kernel.entropy_avail" button in the "Select target for graph" dialog
    Then "kernel entropy_avail" graph should appear in the "machine" page within 30 seconds
    And 10 graphs should be visible within max 20 seconds in the "machine" page

  @monitoring-home-page
  Scenario: Visit Home page and verify that polyana-dashboard is there
    When I visit the Home page
    And I wait for the navigation menu to appear
    Then I wait for the monitoring graphs to appear in the "dashboard" page
    And "Load on all monitored machines" graph in the "dashboard" page should have some values

  @disable-monitoring
  Scenario: Disable monitoring
    When I visit the Machines page
    And I search for "monitored-machine-random"
    And I wait for 2 seconds
    And I click the "monitored-machine-random" "machine"
    #And I click the button "Disable Monitoring" in the "machine" page
    And I click the disable monitoring button for the "machine"
    Then I expect the "Disable Machine Monitoring" dialog to be open within 5 seconds
    When I click the "Disable Monitoring" button in the "Disable Machine Monitoring" dialog
    Then I expect the "Disable Machine Monitoring" dialog to be closed within 5 seconds
    And graphs should disappear within 15 seconds
