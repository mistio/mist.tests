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
    Then I logout of legacy gui

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
    Then I logout of legacy gui

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
    Then I logout

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
    Then I wait for 1 seconds
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Edit Team" in "team" edit form
    And I expect the dialog "Edit Team" is open within 4 seconds
    Then I expect the field "Name" in the dialog with title "Edit Team" to be visible within max 2 seconds
    When I set the value "Rbac Test Team" to field "Name" in "Edit Team" dialog
    And I wait for 1 seconds
    And I click the "Submit" button in the dialog "Edit Team"
    And I expect the dialog "Edit Team" is closed within 4 seconds
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
    Then I logout

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
    Then I logout
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
    Then I logout
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
    Then I logout
    Then I should receive an email at the address "MEMBER2_EMAIL" with subject "[mist.io] Confirm your invitation" within 10 seconds
    And I follow the link contained in the email sent at the address "MEMBER2_EMAIL" with subject "[mist.io] Confirm your invitation"
    Then I enter my rbac_member2 credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    Then I logout
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
    Then I logout
    Given I am logged in to mist.core as rbac_member2
    And I am in the new UI
    When I wait for the dashboard to load
    Then I should see the form to set name for new organization
    Then I logout

  @manage-rules
  Scenario: Manage team rules
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "Rbac_Test" organization context
    When I visit the Keys page
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "PolicyKey" to field "Name" in "key" add form
    Then I click the button "Generate" in "key" add form
    And I wait for 5 seconds
    And I expect for the button "Add" in "key" add form to be clickable within 9 seconds
    When I focus on the button "Add" in "key" add form
    And I click the button "Add" in "key" add form
    Then I expect the "key" edit form to be visible within max 5 seconds
    When I visit the Keys page
    Then "PolicyKey" key should be present within 15 seconds
    Then I visit the Home page
    When I wait for the dashboard to load
    When I visit the Teams page
    When I click the button "+"
    And I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Policy Test Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    And "Policy Test Team" team should be present within 5 seconds
    Then I wait for 2 seconds
    When I click the "Policy Test Team" "team"
    And I expect the "policy" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule "ALLOW" "machine" "all" where tags = "bla=bla"
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "all"
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule "DENY" "key" "edit" where id = "PolicyKey"
    And I click the button "Save Policy" in "policy" edit form
    Then I wait for 3 seconds
    Given rule "0" is "ALLOW" "machine" "all" where tags = "bla=bla"
    Given rule "1" is "ALLOW" "cloud" "all" always
    Given rule "2" is "DENY" "key" "edit" where id = "PolicyKey"
    Then I logout
