@rbac-rules-2
Feature: RBAC-rules-v2

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a Softlayer cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request

  @add-member1
  Scenario: Allow-read-cloud
    When I have given card details if needed
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @view-machine-fail
  Scenario: Verify that member1 cannot view the machine created above
    Given I am logged in to mist.core as rbac_member1
    And I wait for the links in homepage to appear
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 1 clouds added
    When I visit the Machines page
    Then "mistcore_debugger_1" machine should be absent within 5 seconds
    And I logout

  @allow-read-machine
  Scenario: Allow read machine
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "machine" "read"
    And I click the button "Save Policy" in "policy" edit form

  @allow-create-machine
  Scenario: Verify that member1 cannot view the cloud added above
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "machine" "create"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "create resources"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @member1-read-machine-success
  Scenario: Member 1 should now be able to read machine
    Given I am logged in to mist.core as rbac_member1
    When I visit the Machines page
    Then "mistcore_debugger_1" machine should be present within 10 seconds

  @member1-create-machine-success
  Scenario: Member 1 should now be able to create machine
    When I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" drop down
    And I wait for 1 seconds
    And I click the button "Docker" in the "Select Cloud" dropdown
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "rbac-test-machine-random" to field "Machine Name" in "machine" add form
    When I open the "Image" drop down
    And I click the button "mist/ubuntu-14.04:latest" in the "Image" dropdown
    And I wait for 3 seconds
    Then I expect for the button "Launch" in "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in "machine" add form
    And I wait for 2 seconds
    And I click the "Launch" button with id "appformsubmit"
    When I visit the Home page
    And I visit the Machines page
    And I search for "rbac-test-machine-random"
    Then "rbac-test-machine-random" machine state has to be "running" within 50 seconds
    And I logout

  @owner-deletes-allow-read-machine-rule
  Scenario: Owner deletes rule "ALLOW" "read" "machine"
    Given I am logged in to mist.core as rbac_owner
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds

  @owner-allows-edit-script
  Scenario: Owner creates rule "ALLOW" "script" "edit"
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "edit"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    And script "TestScript" is added via API request
    Then I logout

  @member-reads-machine-fail
  Scenario: Member cannot view the machine
    Given I am logged in to mist.core as rbac_member1
    When I visit the Machines page
    Then "mistcore_debugger_1" machine should be absent within 5 seconds

  @member-edit-script-success
  Scenario: Member 1 should be able to edit the script
    When I visit the Scripts page
    And I click the "TestScript" "script"
    Then I expect the "script" edit form to be visible within max 5 seconds
    When I click the button "Edit" in the "script" page actions menu
    Then I expect the dialog "Edit Script" is open within 4 seconds
    When I set the value "Second" to field "Name" in "Edit Script" dialog
    And I click the "Submit" button in the dialog "Edit Script"
    Then I expect the dialog "Edit Script" is closed within 4 seconds
    When I visit the Home page
    And I wait for 1 seconds
    And I visit the Scripts page
    Then "TestScript" script should be absent within 5 seconds
    And "Second" script should be present within 5 seconds
