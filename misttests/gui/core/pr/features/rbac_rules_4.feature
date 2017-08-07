@rbac-rules-4
Feature: RBAC-rules-v4

#TODO: Add member1 via API
#TODO: Add key via API

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a cloud and a script
    Given rbac members, organization and team are initialized
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request
    And script "touch_kati" is added via API request

  @add-member1
  Scenario: Add member1 and add DENY-READ-ALL and ALLOW-ALL-ALL.
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I click the button "Invite Members" in "team" edit form
    Then I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER1_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    When I click the button "Add" in "members" add form
    Then I expect the "team" edit form to be visible within max 5 seconds
    And user with email "MEMBER1_EMAIL" should be pending
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
