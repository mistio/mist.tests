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

  @manage-team
  Scenario: Owner creates/renames/deletes a team
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    When I visit the Teams page
    When I click the button "+"
    And I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Test Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Edit Team" from the menu of the "team" edit form
    And I expect the dialog "Rename Team" is open within 4 seconds
    Then I expect the field "Name" in the dialog with title "Rename Team" to be visible within max 2 seconds
    When I set the value "Rbac Test Team" to field "Name" in "Rename Team" dialog
    And I click the "Submit" button in the dialog "Rename Team"
    And I expect the dialog "Rename Team" is closed within 4 seconds
    Then I visit the Teams page
    And "Test Team" key should be absent within 5 seconds
    And "Rbac Test Team" team should be present within 5 seconds
    When I click the "Rbac Test Team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Delete Team" from the menu of the "team" edit form
    And I expect the dialog "Delete Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Team"
    Then I expect the dialog "Delete Team" is closed within 4 seconds
    And I visit the Teams page
    And "Rbac Test Team" team should be absent within 5 seconds
    Then I wait for 2 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu

  @manage-members
  Scenario: Owner invites and deletes a team member
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    When I visit the Teams page
    When I click the button "+"
    And I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Test Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Invite Members" in "team" edit form
    And I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER1_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    And I click the button "Add" in "members" add form
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER1_EMAIL" should be pending
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
    And I follow the link contained in the email sent at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation"
    Then I click the email button in the landing page popup
    Then I enter my rbac_member1 credentials for login
    And I click the sign in button in the landing page popup
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Invite Members" in "team" edit form
    And I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER2_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    And I click the button "Add" in "members" add form
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER2_EMAIL" should be pending
    And user with email "MEMBER1_EMAIL" should be confirmed
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu
    Then I should receive an email at the address "MEMBER2_EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
    And I follow the link contained in the email sent at the address "MEMBER2_EMAIL" with subject "[mist.io] Confirm your invitation"
    Then I enter my rbac_member2 credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER2_EMAIL" should be confirmed
    When I delete user "MEMBER2_EMAIL" from team
    And I expect the dialog "Delete Member from Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Member from Team"
    And I expect the dialog "Delete Member from Team" is closed within 4 seconds
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Logout" in the user menu
    And I wait for 2 seconds

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