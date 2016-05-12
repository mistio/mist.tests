@rbac

Feature: RBAC

  @manage-team
  Scenario: Manage team
    Given I am logged in to mist.core as rbac_owner
    And I switch to the ORG organization
    When I visit the Teams page after the Teams counter has loaded
    When I click the button "Create team"
    Then I expect for "add-team" collapsible to appear within max 5 seconds
    Then I give a random team name for new team
    Then I click the button "Add"
    Then I expect for "add-team" collapsible to disappear within max 5 seconds
    Then I search for the random team name i gave before
    Then I should see the team added within 5 seconds
    Then I choose the randomly created team
    And I click the button "Edit"
    Then I expect for "team-edit-popup-popup" popup to appear within max 5 seconds
    Then I give a random team name for edit team
    And I click the "save" button inside the "Edit Team" popup
    Then I expect for "team-edit-popup-popup" popup to disappear within max 5 seconds
    Then I should see the team added within 5 seconds
    Then I search for the random team name i gave before
    Then I choose the randomly created team
    And I click the button "Delete"
    And I expect for "dialog-popup" modal to appear within max 4 seconds
    And I click the button "Yes"
    And I clear the search bar
    Then the random team should be deleted

  @manage-members
  Scenario: Manage members and team from single team page
    Given I am logged in to mist.core as rbac_owner
    And I switch to the ORG organization
    When I visit the Teams page after the Teams counter has loaded
    When I click the button "Create team"
    Then I expect for "add-team" collapsible to appear within max 5 seconds
    Then I give a random team name for new team
    Then I click the button "Add"
    Then I expect for "add-team" collapsible to disappear within max 5 seconds
    Then I choose the random team
    And I click the button "Invite Member"
    Then I give the rbac_member1 email
    And I click the button "Send"
    Then I should receive an email at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
    Then I expect the rbac_member1 to appear on the team members within max 5 seconds
    Then I click the button to delete the rbac_member1
    And I click the button "Yes"
    Then I expect for the rbac_member1 to be deleted after 5 seconds
    Then I should receive an email at the address "RBAC_MEMBER_EMAIL" with subject "Your status in an organization has changed" within 10 seconds
    Then I click the button "Edit"
    Then I expect for "team-edit-popup-popup" popup to appear within max 5 seconds
    Then I give a random team name for edit team
    And I click the "save" button inside the "Edit Team" popup
    Then I expect for "team-edit-popup-popup" popup to disappear within max 5 seconds
    Then I should see the team name changed within 5 seconds
    And I click the button "Delete"
    And I expect for "dialog-popup" modal to appear within max 4 seconds
    And I click the button "Yes"
    Then I wait for 2 seconds
    And I clear the search bar
    Then the random team should be deleted

  @manage-rules
  Scenario: Manage team rules
    Given I am logged in to mist.core as rbac_owner
    And I switch to the ORG organization
    When I visit the Teams page after the Teams counter has loaded
    When I click the button "Create team"
    Then I expect for "add-team" collapsible to appear within max 5 seconds
    Then I give a random team name for new team
    Then I click the button "Add"
    Then I expect for "add-team" collapsible to disappear within max 5 seconds
    Then I choose the random team
    Then I click the button "Add Rule"
    Then I click the button "Deny"
    Then I expect for "policy-rule-operator-popup" popup to appear within max 5 seconds
    Then I click the button "Allow"
    Then I expect for "policy-rule-operator-popup" popup to disappear within max 5 seconds
    Then I click the button "All"
    Then I expect for "policy-rule-resource-popup" popup to appear within max 5 seconds
    Then I click the button "Cloud"
    Then I expect for "policy-rule-resource-popup" popup to disappear within max 5 seconds
    Then I click the button "Save rules"
    And I click the button "Delete"
    And I expect for "dialog-popup" modal to appear within max 4 seconds
    And I click the button "Yes"
    Then I wait for 2 seconds
