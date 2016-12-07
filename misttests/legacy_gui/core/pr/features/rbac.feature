@rbac
Feature: RBAC

  # owner signs up
  @owner-signup
  Scenario: Owner sign-up process
    Given I am not logged in to mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my rbac_owner credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "RBAC_OWNER_EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    And I follow the link contained in the email sent at the address "RBAC_OWNER_EMAIL" with subject "[mist.io] Confirm your registration"
    Then I enter my rbac_owner credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I am in the legacy UI
    And I wait for the mist.io splash page to load

  # user (with no owner privileges) signs up
  @user-signup
  Scenario: User sign-up process
    Given I am not logged in to mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my rbac_member credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    And I follow the link contained in the email sent at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your registration"
    Then I enter my rbac_member credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I am in the legacy UI
    And I wait for the mist.io splash page to load

  # owner creates an organization
  @create-org
  Scenario: Organization creation
    Given I am logged in to mist.core as rbac_owner
    And I am in the legacy UI
    When I click the gravatar
    Then I click the button "ADD ORGANIZATION"
    And I expect for "organization-add-popup" popup to appear within max 3 seconds
    Then I give the organization name
    And I click the button "ADD"
    And I expect for "dialog-popup" modal to appear within max 3 seconds
    And I click the button "OK"
    And I wait for the mist.io splash page to load
    # we've landed at the newly created organization page
    # now let's switch back to personal context
    And I switch to personal context
    # let's try to create the same organization again
    # expecting an error
    Given I am logged in to mist.core as rbac_owner
    When I click the gravatar
    Then I click the button "ADD ORGANIZATION"
    And I expect for "organization-add-popup" popup to appear within max 3 seconds
    Then I give the organization name
    And I click the button "ADD"
    Then I should get an Organization Name Exists error

  @add-org-cloud
  Scenario: Add cloud in organization context
    Given I am logged in to mist.core as rbac_owner
    And I am in the legacy UI
    And I switch to the ORG organization
    Given "EC2" cloud has been added
    Then I logout

  @manage-team
  Scenario: Manage member and team from single team page
    Given I am logged in to mist.core as rbac_owner
    And I am in the legacy UI
    And I switch to personal context
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
    And I click the button "Invite Member"
    Then I give the rbac_member1 email
    And I click the button "Send"
    Then I expect the rbac_member1 to appear on the team members within max 5 seconds
    Then I click the button to delete the rbac_member1
    And I click the button "Yes"
    Then I expect for the rbac_member1 to be deleted after 5 seconds
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

  @manage-members
  Scenario: Invite mist.io and non-mist.io members
    Given I am logged in to mist.core as rbac_owner
    And I am in the legacy UI
    And I switch to personal context
    Given I am logged in to mist.core as rbac_owner
    And I switch to the ORG organization
    When I visit the Teams page after the Teams counter has loaded
    When I click the button "Create team"
    Then I expect for "add-team" collapsible to appear within max 5 seconds
    Then I give a random team name for new team
    Then I click the button "Add"
    Then I expect for "add-team" collapsible to disappear within max 5 seconds
    Then I choose the random team
    # owner invites rbac_member to join the organization
    And I click the button "Invite Member"
    Then I give the rbac_member1 email
    And I click the button "Send"
    Then I expect the rbac_member1 to appear on the team members within max 5 seconds
    Then I should receive an email at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
    And I wait for 3 seconds
    # owner invites a user to join the organization
    # after signing-up with mist.io
    And I click the button "Invite Member"
    Then I give the reg_member1 email
    And I click the button "Send"
    Then I expect the reg_member1 to appear on the team members within max 5 seconds
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
    And I wait for 3 seconds
    Then I logout
    # rbac_member confirms invitation
    Given I am not logged in to mist.core
    And I follow the link contained in the email sent at the address "RBAC_MEMBER_EMAIL" with subject "[mist.io] Confirm your invitation"
    Then I click the email button in the landing page popup
    Then I enter my rbac_member credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the mist.io splash page to load
    And I switch to personal context
    Given I am logged in to mist.core as rbac_member
    And I switch to the ORG organization
    Then I logout
    # reg_member confirms invitation after signing up with mist.io
    Given I am not logged in to mist.core
    And I follow the link contained in the email sent at the address "EMAIL" with subject "[mist.io] Confirm your invitation"
    Then I enter my standard credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I wait for the mist.io splash page to load
    And I switch to personal context
    Given I am logged in to mist.core as reg_member
    And I switch to the ORG organization
    Then I logout
    # login in back as owner to verify invitation status
    Given I am not logged in to mist.core
    And I refresh the current page
    Given I am logged in to mist.core as rbac_owner
    When I visit the Teams page after the Teams counter has loaded
    # verify that all pending statuses are gone
    Then I choose the random team
    Then I expect to see no pending member invitations

  @manage-rules
  Scenario: Manage team rules
    Given I am logged in to mist.core as rbac_owner
    And I am in the legacy UI
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
