@rbac-rules-4
Feature: RBAC-rules-v4

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a cloud and a script
    Given rbac members, organization and team are initialized
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request
    And script "touch_kati" is added via API request

  @add-member1
    Scenario: Add DENY-READ-ALL and ALLOW-ALL-ALL rules.
      When I visit the Teams page
      And I click the "Test team" "team"
      Then I expect the "team" edit form to be visible within max 5 seconds
      When I focus on the button "Add a new rule" in "policy" edit form
      And I click the button "Add a new rule" in "policy" edit form
      And I wait for 1 seconds
      Then I add the rule always "DENY" "all" "READ"
      And I click the button "Save Policy" in "policy" edit form
      And I wait for 2 seconds
      When I focus on the button "Add a new rule" in "policy" edit form
      And I click the button "Add a new rule" in "policy" edit form
      And I wait for 1 seconds
      Then I add the rule always "ALLOW" "all" "all"
      And I click the button "Save Policy" in "policy" edit form
      And I wait for 1 seconds
      Then I logout

  @view-cloud-and-script-fail
  Scenario: Verify that member1 cannot view the script and the cloud added above, since 'DENY-READ-ALL superseeds 'ALLOW-ALL-ALL rule'
    Given I am logged in to mist.core as rbac_member1
    And I wait for the links in homepage to appear
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 0 clouds added
    When I visit the Scripts page
    Then "touch_kati" script should be absent within 5 seconds
    And I logout

  @deny-all-script
  Scenario: Delete previous rules and add DENY-ALL-SCRIPT and ALLOW-ALL-ALL.
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I remove the rule with index "0"
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "DENY" "SCRIPT" "ALL"
    #And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    Then I logout

  @view-cloud-success-and-script-fail
  Scenario: Verify that member1 cannot view the script added above, but can see the docker cloud
    Given I am logged in to mist.core as rbac_member1
    Then I should have 1 clouds added
    When I visit the Scripts page
    Then "touch_kati" script should be absent within 5 seconds
    And I logout

  @deny-view-cloud-on-tags
  Scenario: Tag Docker cloud, delete previous rules and add DENY-VIEW-CLOUD and ALLOW-ALL-ALL.
    Given I am logged in to mist.core
    When I open the cloud menu for "Docker"
    Then I expect the "cloud" edit form to be visible within max 5 seconds
    When I click the button "Tag" in "cloud" edit form
    Then I expect for the tag popup to open within 4 seconds
    When I add a tag with key "rbac" and value "test"
    And I click the button "Save" in the tag menu
    Then I expect for the tag popup to close within 4 seconds
    And I ensure that the "cloud" has the tags "rbac:test" within 5 seconds
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I remove the rule with index "0"
    And I wait for 1 seconds
    And I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    And I add the rule "DENY" "CLOUD" "READ" where tags = "rbac=test"
    And I wait for 2 seconds
    And I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    Then I logout

  @view-cloud-fail
  Scenario: Verify that member1 cannot view the cloud that has been tagged with "rbac-test"
    Given I am logged in to mist.core as rbac_member1
    Then I should have 0 clouds added
    And I logout

  @delete-rule
  Scenario: Delete rule DENY-VIEW-CLOUD
    Given I am logged in to mist.core
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I remove the rule with index "0"
    And I wait for 1 seconds
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    And I logout

  @view-cloud-success
  Scenario: Verify that member1 can now view the cloud, since the only existing rule is ALLOW-ALL-ALL
    Given I am logged in to mist.core as rbac_member1
    Then I should have 1 clouds added
