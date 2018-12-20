@rbac-rules-3
Feature: RBAC-rules-v3

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request
    And script "touch_kati" is added via API request

  @add-member1
  Scenario: Add ALLOW-script-ALL
    When I have given card details if needed
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "all"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds

  @add-non-visible-team
  Scenario: Owner creates a non-visible team
    When I visit the Teams page
    And I click the button "+"
    Then I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Non-visible Team" to field "Name" in "Add Team" dialog
    And I click the toggle button with id "visible" in the dialog "Add Team"
    And I click the "Add" button in the dialog "Add Team"
    And I visit the Teams page
    Then "Non-visible Team" team should be present within 5 seconds
    And "Test Team" team should be present within 5 seconds
    Then I logout

  @view-and-delete-script-success
  Scenario: Verify that member1 cannot view the team created above but can delete script
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    And "Non-visible Team" team should be absent within 5 seconds
    When I visit the Scripts page
    Then "touch_kati" script should be present within 5 seconds
    When I select list item "touch_kati" script
    And I click the action "Delete" from the script list actions
    And I expect the dialog "Delete Script" is open within 4 seconds
    And I wait for 2 seconds
    And I click the "Delete" button in the dialog "Delete Script"
    And I expect the dialog "Delete Script" is closed within 4 seconds
    Then "touch_kati" script should be absent within 5 seconds
    And I logout

  @allow-all-read
  Scenario: ALLOW-ALL-READ
    Given I am logged in to mist as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @member1-view-cloud-and-machine-success
  Scenario: Verify that member1 can view cloud and machine
    Given I am logged in to mist as rbac_member1
    When I visit the Machines page
    Then "Docker" machine should be present within 5 seconds
    When I visit the Home page
    Then I should have 1 clouds added
    Then I logout

  @deny-read-cloud-by-id
  Scenario: DENY-CLOUD-WHERE-ID-DOCKER
    Given I am logged in to mist as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I remove the rule with index "0"
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    And I add the rule "DENY" "CLOUD" "READ" where id = "Docker"
    And I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @member1-view-cloud-and-machine-success
  Scenario: Verify that member1 cannot view docker cloud
    Given I am logged in to mist as rbac_member1
    Then I should have 0 clouds added
