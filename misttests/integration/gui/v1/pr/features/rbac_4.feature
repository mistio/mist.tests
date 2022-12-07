@rbac-4
Feature: RBAC-rules-v4

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a cloud and a script
    Given rbac members, organization and team are initialized
    Given I am logged in to mist
    Given cloud "Docker" has been added via API request
    And script "touch_kati" has been added via API request

  @add-member1
    Scenario: Add DENY-READ-ALL and ALLOW-ALL-ALL rules.
      When I have given card details if needed
      And I visit the Teams page
      And I wait for 1 seconds
      And I click the "Test team" "team"
      Then I expect the "team" page to be visible within max 5 seconds
      When I click the button "Add a new rule" in the "team" page
      And I wait for 1 seconds
      Then I add the rule always "DENY" "all" "READ"
      And I click the button "Save Policy" in the "team" page
      And I wait for 2 seconds
      When I click the button "Add a new rule" in the "team" page
      And I wait for 1 seconds
      Then I add the rule always "ALLOW" "all" "all"
      And I click the button "Save Policy" in the "team" page
      And I wait for 1 seconds
      Then I logout

  @view-cloud-and-script-fail
  Scenario: Verify that member1 cannot view the script and the cloud added above, since 'DENY-READ-ALL superseeds 'ALLOW-ALL-ALL rule'
    Given I am logged in to mist as rbac_member1
    And the "Teams" navigation menu item should not exist
    And the "Clouds" navigation menu item should not exist
    And the "Machines" navigation menu item should not exist
    And the "Scripts" navigation menu item should not exist
    And I logout

  @deny-all-script
  Scenario: Delete previous rules and add DENY-ALL-SCRIPT and ALLOW-ALL-ALL.
    Given I am logged in to mist
    When I visit the Teams page
    And I wait for 1 seconds
    And I click the "Test team" "team"
    Then I expect the "team" page to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I remove the rule with index "0"
    When I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "DENY" "SCRIPT" "ALL"
    #And I click the button "Save Policy" in the "team" page
    And I wait for 2 seconds
    When I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in the "team" page
    And I wait for 1 seconds
    Then I logout

  @view-cloud-success-and-script-fail
  Scenario: Verify that member1 cannot view the script added above, but can see the docker cloud
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I ensure that I am in the "ORG_NAME" organization context
    Then I should have 1 clouds added
    And the "Scripts" navigation menu item should not exist
    And I logout

  @deny-view-cloud-on-tags
  Scenario: Tag Docker cloud, delete previous rules and add DENY-VIEW-CLOUD and ALLOW-ALL-ALL.
    Given I am logged in to mist
    When I open the cloud page for "Docker"
    Then I expect the "cloud" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "cloud" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    When I add a tag with key "rbac" and value "test"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    And I ensure that the "cloud" has the tags "rbac:test" within 5 seconds
    When I visit the Teams page
    And I wait for 1 seconds
    And I click the "Test team" "team"
    Then I expect the "team" page to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I remove the rule with index "0"
    And I wait for 1 seconds
    When I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    And I add the rule "DENY" "CLOUD" "READ" where tags = "rbac=test"
    And I wait for 2 seconds
    And I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in the "team" page
    And I wait for 1 seconds
    Then I logout

  @view-cloud-fail
  Scenario: Verify that member1 cannot view the cloud that has been tagged with "rbac-test"
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I ensure that I am in the "ORG_NAME" organization context
    Then I should have 0 clouds added
    When I visit the Scripts page
    Then "touch_kati" script should be present within 3 seconds
    And I logout

  @delete-rule
  Scenario: Delete rule DENY-VIEW-CLOUD, and add DENY-ALL-ALL where tags="view=denied". Tag the script as "denied"
    Given I am logged in to mist
    When I visit the Teams page
    And I wait for 1 seconds
    And I click the "Test team" "team"
    Then I expect the "team" page to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I remove the rule with index "0"
    And I wait for 1 seconds
    When I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    And I add the rule "DENY" "ALL" "ALL" where tags = "view=denied"
    And I wait for 2 seconds
    And I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in the "team" page
    And I wait for 1 seconds
    When I visit the Scripts page
    And I wait for 1 seconds
    And I click the "touch_kati" "script"
    Then I expect the "script" page to be visible within max 5 seconds
    When I click the "Tag" action button in the "script" page
    Then I expect the "Tags" dialog to be open within 4 seconds
    And I wait for 1 seconds
    And I add a tag with key "view" and value "denied"
    And I click the "Save" button in the "Tags" dialog
    Then I expect the "Tags" dialog to be closed within 4 seconds
    Then I ensure that the "script" has the tags "view:denied" within 5 seconds
    And I logout

  @view-cloud-success
  Scenario: Verify that member1 can now view the cloud but cannot view the script
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I ensure that I am in the "ORG_NAME" organization context
    Then I should have 1 clouds added
    When I visit the Scripts page
    Then "touch_kati" script should be absent within 5 seconds
