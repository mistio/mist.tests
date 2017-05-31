@monitoring-locally
Feature: Monitoring tested locally


  @enable-monitoring
  Scenario: Create Machine,deploy monitoring agent and check the graphs
    Given I am logged in to mist.core

    # add fullstack_key via API

    # And cloud "Mist Debugger" has been added via API request

    # also dont run if wrong vault creds given...


#machine_ip
#:
#"mist_debugger"
#machine_key
#:
#"037b299a8f0648bab1a052932da060b0"
#machine_port
#:
#22
#machine_user
#:
#"root"
#monitoring
#:
#true
#operating_system
#:
#"unix"
#provider
#:
#"bare_metal"
#remote_desktop_port
#:
#3389
#title
#:
#"Local_Monitoring"

    When I visit the Machines page
    And I wait for 3 seconds
    When I click the "Local_Monitoring" "machine"
    And I wait for 2 seconds
    Then 9 graphs should be visible within max 30 seconds
    And I wait for the graphs to appear

  @add-entropy-graph
  Scenario: Add custom graph and make sure an extra graph is visible
    When I refresh the page
    And I wait for 10 seconds
    And I click the button "Add Graph"
    Then I expect for "selectTarget" modal to appear within max 20 seconds
    And I expect the metric buttons to appear within 30 seconds
    When I click the "entropy" button inside the popup with id "selectTarget"
    And I wait for 6 seconds
    Then "entropy" graph should appear within 30 seconds
    And 10 graphs should be visible within max 20 seconds
    When I wait for 3 seconds
    And I focus on the "entropy" graph
    Then "entropy" graph should have some values

  @monitoring-home-page
  Scenario: Visit Home page and verify that polyana-dashboard is there
    When I visit the Home page
    And I wait for the links in homepage to appear
    Then I wait for the graphs to appear

  @incidents
  Scenario: Add a rule that will be triggered immediately, and verify that an incident will appear in home page
    When I focus on the "add new rule" button
    And I click the button "add new rule"
    Then I expect for "newrule" to be visible within max 20 seconds
    And I click the "metricName" rule
#    And I click the "RAM" button in the dropdown with id "metricName"
    When I fill "0" as metric value
    And I save the rule
#
#  @disable-monitoring
#  Scenario: Disable monitoring
#    When I visit the Machines page
#    And I click the "monitored-machine-random" "machine"
#    And I wait for 2 seconds
#    And I click the "Disable Monitoring" button
#    And I wait for 2 seconds
#    And I click the "Disable Monitoring" button
#    Then I expect the dialog "Disable Machine Monitoring" is open within 5 seconds
#    When I click the "Disable Monitoring" button in the dialog "Disable Machine Monitoring"
#    Then I expect the dialog "Disable Machine Monitoring" is closed within 5 seconds
#    And graphs should disappear within 15 seconds
