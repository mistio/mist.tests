@rbac
Feature: RBAC

  @owner-signup
  Scenario: Organization Owner signs up
    When I visit mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my rbac_owner credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "OWNER_EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    And I follow the link contained in the email sent at the address "OWNER_EMAIL" with subject "[mist.io] Confirm your registration"
    Then I enter my rbac_owner credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I wait for the mist.io splash page to load
    Then I logout

  @member1-signup
  Scenario: Member1 of organization signs up
    When I visit mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my rbac_member1 credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    And I follow the link contained in the email sent at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your registration"
    Then I enter my rbac_member1 credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I wait for the mist.io splash page to load
    Then I logout

  @create-org
  Scenario: Owner creates a new organization
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Add Organisation" in the user menu
    And I expect the dialog "Add Organization" is open within 4 seconds
    And I wait for 1 seconds
    When I set the value "Rbac_Test" to field "Name" in "Add Organization" dialog
    And I click the "Add" button in the dialog "Add Organization"
    And I wait for 1 seconds
    And I click the "Switch" button in the dialog "Add Organization"
    Then I expect the dialog "Add Organization" is closed within 4 seconds
    When I wait for the dashboard to load
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu

  @manage-teams
  Scenario: Owner manages the teams of the organization
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    And I wait for 3 seconds


#  @manage-team
#  Scenario: Manage member and team from single team page
#    Given I am logged in to mist.core as rbac_owner
#    And I switch to the ORG organization
#    When I visit the Teams page after the Teams counter has loaded
#    When I click the button "Create team"
#    Then I expect for "add-team" collapsible to appear within max 5 seconds
#    Then I give a random team name for new team
#    Then I click the button "Add"
#    Then I expect for "add-team" collapsible to disappear within max 5 seconds
#    Then I search for the random team name i gave before
#    Then I should see the team added within 5 seconds
#    Then I choose the randomly created team
#    And I click the button "Invite Member"
#    Then I give the rbac_member1 email
#    And I click the button "Send"
#    Then I expect the rbac_member1 to appear on the team members within max 5 seconds
#    Then I click the button to delete the rbac_member1
#    And I click the button "Yes"
#    Then I expect for the rbac_member1 to be deleted after 5 seconds
#    Then I click the button "Edit"
#    Then I expect for "team-edit-popup-popup" popup to appear within max 5 seconds
#    Then I give a random team name for edit team
#    And I click the "save" button inside the "Edit Team" popup
#    Then I expect for "team-edit-popup-popup" popup to disappear within max 5 seconds
#    Then I should see the team name changed within 5 seconds
#    And I click the button "Delete"
#    And I expect for "dialog-popup" modal to appear within max 4 seconds
#    And I click the button "Yes"
#    Then I wait for 2 seconds
#    And I clear the search bar
#    Then the random team should be deleted
#
#  @manage-members
#  Scenario: Invite mist.io and non-mist.io members
#    Given I am logged in to mist.core as rbac_owner
#    And I switch to personal context
#    Given I am logged in to mist.core as rbac_owner
#    And I switch to the ORG organization
#    When I visit the Teams page after the Teams counter has loaded
#    When I click the button "Create team"
#    Then I expect for "add-team" collapsible to appear within max 5 seconds
#    Then I give a random team name for new team
#    Then I click the button "Add"
#    Then I expect for "add-team" collapsible to disappear within max 5 seconds
#    Then I choose the random team
#    # owner invites rbac_member to join the organization
#    And I click the button "Invite Member"
#    Then I give the rbac_member1 email
#    And I click the button "Send"
#    Then I expect the rbac_member1 to appear on the team members within max 5 seconds
#    Then I should receive an email at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
#    And I wait for 3 seconds
#    # owner invites a user to join the organization
#    # after signing-up with mist.io
#    And I click the button "Invite Member"
#    Then I give the reg_member1 email
#    And I click the button "Send"
#    Then I expect the reg_member1 to appear on the team members within max 5 seconds
#    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
#    And I wait for 3 seconds
#    Then I logout
#    # rbac_member confirms invitation
#    Given I am not logged in to mist.core
#    And I follow the link contained in the email sent at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your invitation"
#    Then I click the email button in the landing page popup
#    Then I enter my rbac_member credentials for login
#    And I click the sign in button in the landing page popup
#    Then I wait for the mist.io splash page to load
#    And I switch to personal context
#    Given I am logged in to mist.core as rbac_member
#    And I switch to the ORG organization
#    Then I logout
#    # reg_member confirms invitation after signing up with mist.io
#    Given I am not logged in to mist.core
#    And I follow the link contained in the email sent at the address "EMAIL" with subject "[mist.io] Confirm your invitation"
#    Then I enter my standard credentials for signup_password_set
#    And I click the submit button in the landing page popup
#    And I wait for the mist.io splash page to load
#    And I switch to personal context
#    Given I am logged in to mist.core as reg_member
#    And I switch to the ORG organization
#    Then I logout
#    # login in back as owner to verify invitation status
#    Given I am not logged in to mist.core
#    And I refresh the page
#    Given I am logged in to mist.core as rbac_owner
#    When I visit the Teams page after the Teams counter has loaded
#    # verify that all pending statuses are gone
#    Then I choose the random team
#    Then I expect to see no pending member invitations
#
#  @manage-rules
#  Scenario: Manage team rules
#    Given I am logged in to mist.core as rbac_owner
#    When I visit the Teams page after the Teams counter has loaded
#    When I click the button "Create team"
#    Then I expect for "add-team" collapsible to appear within max 5 seconds
#    Then I give a random team name for new team
#    Then I click the button "Add"
#    Then I expect for "add-team" collapsible to disappear within max 5 seconds
#    Then I choose the random team
#    Then I click the button "Add Rule"
#    Then I click the button "Deny"
#    Then I expect for "policy-rule-operator-popup" popup to appear within max 5 seconds
#    Then I click the button "Allow"
#    Then I expect for "policy-rule-operator-popup" popup to disappear within max 5 seconds
#    Then I click the button "All"
#    Then I expect for "policy-rule-resource-popup" popup to appear within max 5 seconds
#    Then I click the button "Cloud"
#    Then I expect for "policy-rule-resource-popup" popup to disappear within max 5 seconds
#    Then I click the button "Save rules"
#    And I click the button "Delete"
#    And I expect for "dialog-popup" modal to appear within max 4 seconds
#    And I click the button "Yes"
#    Then I wait for 2 seconds