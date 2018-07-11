@rules
Feature: rules

	@add-rule-apply-to-every-machine
	 Scenario: Add rule from rules section that applies on all machines. Verify it is visible in single machine page and it works
	    Given I am logged in to mist.core
	    And cloud "Docker" has been added via API request
	    And key "Key1" has been added via API request
	    And I have given card details if needed
		When I visit the machines page
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
	    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
	    When I focus on the button "Launch" in "machine" add form
	    And I wait for 2 seconds
	    And I click the "Launch" button with id "appformsubmit"
	    And I wait for 1 seconds
	    And I visit the Home page
	    And I visit the Machines page
	    And I search for "monitored-machine-random"
	    Then "monitored-machine-random" machine state has to be "running" within 30 seconds
	    When I click the "monitored-machine-random" "machine"
	    And I wait for 2 seconds
	    And I click the button "Enable Monitoring"
	    And I wait for 5 seconds
	    Then I wait for the graphs to appear
	    And 9 graphs should be visible within max 30 seconds
	    When I visit the Rules page
	    And I click the button "add new rule"
	    And I wait for 1 seconds
	    And I click the "apply on" button with id "apply-on"
	    And I click the "every machine" button in the dropdown with id "apply-on-"
	    And I click the "target" button with id "target-0"
	    And I click the "Load" button in the dropdown with id "target-0"
	    And I wait for 1 seconds
	    And I click the "<" button in the dropdown with id "operator-0"
	    And I type "10" in input with id "threshold-0"
    	And I click the "actionsDropdown" button with id "actionsDropdown"
    	And I click the button "alert" in the "actionsDropdown" dropdown
	    And I open the "teams" mist-dropdown
	    And I select "Owners" in "teams" mist-dropdown
	    And I wait for 2 seconds
    	And I save the rule
    	And I visit the Machines page
	    And I search for "monitored-machine-random"
	    And I click the "monitored-machine-random" "machine"
	    And I scroll to the bottom of the page
    	And I wait for 2 seconds
		Then rule "if load < 10 for any value then alert team Owners" should be present
		Then I should receive an email at the address "EMAIL" with subject "[mist.io] *** WARNING *** from monitored-machine-random: Load" within 150 seconds
		#When I visit the machines page
		#And I search for "monitored-machine-random"
		#Then "monitored-machine-random" machine should be absent within 120 seconds

	@add-rule-apply-to-tagged-machine
	 Scenario: Add rule from rules section that applies on tagged machine. Verify it is visible in single machine page and it works


# T
