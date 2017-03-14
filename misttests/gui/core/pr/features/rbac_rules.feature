@rbac-rules
Feature: RBAC

  @create-users-org-team
  Scenario: Owner creates a new organization and adds a Softlayer cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist.core
    Given "SoftLayer" cloud has been added

  @add-member1
  Scenario: Add member1
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
    Then I logout

  @view-cloud-fail
  Scenario: Verify that member1 cannot view the cloud added above
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation" within 30 seconds
    And I follow the link inside the email
    Then I enter my rbac_member1 credentials for login
    And I click the sign in button in the landing page popup
    Given that I am redirected within 10 seconds
    And I wait for the dashboard to load
    When I ensure that I am in the "ORG_NAME" organization context
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 0 clouds added
    And I logout

   @allow-read-cloud
   Scenario: Allow reading a cloud
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds

  @allow-read-script
  Scenario: Allow reading a script and add a script
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Given script "TestScript" is added
    Then I logout

  @member1-view-cloud-success
  Scenario: Verify that member1 can view a cloud
    Given I am logged in to mist.core as rbac_member1
    And I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 1 clouds added

  @member1-add-cloud-fail
  Scenario: Member1 cannot add cloud
    When I click the new cloud button
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "Vultr" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "Vultr" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    And I click the button "Add Cloud" in "cloud" add form
    And I wait for 2 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then I should have 1 clouds added

  @member1-view-script-success
  Scenario: Member 1 should be able to view the script
    When I visit the Scripts page
    And I wait for 2 seconds
    Then I click the "TestScript" "script"

  @member1-edit-script-fail
  Scenario: Member 1 should not be able to edit the script
    And I expect the "script" edit form to be visible within max 5 seconds
    Then I logout

  @allow-add-cloud
  Scenario: Allow adding a cloud
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "add"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds

  @allow-edit-script
  Scenario: Allow editing a script
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "edit"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

  @member1-add-cloud-success
  Scenario: Member 1 should now be able to add cloud
    Given I am logged in to mist.core as rbac_member1
    Then I ensure that I am in the "ORG_NAME" organization context
    When I click the new cloud button
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "Vultr" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "Vultr" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    And I click the button "Add Cloud" in "cloud" add form
    Then I wait for 2 seconds
    Then I visit the Home page
    Then I wait for the dashboard to load
    Then I should have 2 clouds added

  @member1-delete-cloud-fail
  Scenario: Member 1 should not be able to delete cloud
    When I wait for 2 seconds
    When I open the cloud menu for "SoftLayer"
    And I click the "delete cloud" button
    And I expect the dialog "Delete SoftLayer" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete SoftLayer"
    And I expect the dialog "Delete SoftLayer" is closed within 4 seconds
    And I wait for 3 seconds
    Then I visit the Home page
    # deletion did not work
    Then I should have 2 clouds added

  @member1-edit-script-success
  Scenario: Member 1 should be able to edit the script
    When I visit the Scripts page
    Then I click the "TestScript" "script"
    And I expect the "script" edit form to be visible within max 5 seconds
    Then I click the button "Edit Script" from the menu of the "script" edit form
    And I expect the dialog "Edit Script" is open within 4 seconds
    When I set the value "Second" to field "Name" in "Edit Script" dialog
    And I click the "Submit" button in the dialog "Edit Script"
    And I expect the dialog "Edit Script" is closed within 4 seconds
    Then I visit the Home page
    And I wait for 2 seconds
    Then I visit the Scripts page
    And "TestScript" script should be absent within 5 seconds
    And "Second" script should be present within 5 seconds

#  @manage-rules
#  Scenario: Manage team rules
#    When I visit the teams page
#    When I click the "Rbac Test Team" "team"
#    And I expect the "policy" edit form to be visible within max 5 seconds
#    When I focus on the button "Add a new rule" in "policy" edit form
#    Then I click the button "Add a new rule" in "policy" edit form
#    And I wait for 1 seconds
#    Then I add the rule "ALLOW" "machine" "all" where tags = "bla=bla"
#    When I focus on the button "Add a new rule" in "policy" edit form
#    Then I click the button "Add a new rule" in "policy" edit form
#    And I wait for 1 seconds
#    Then I add the rule always "ALLOW" "cloud" "all"
#    When I focus on the button "Add a new rule" in "policy" edit form
#    Then I click the button "Add a new rule" in "policy" edit form
#    And I wait for 1 seconds
#    Then I add the rule "DENY" "key" "edit" where id = "PolicyKey"
#    And I click the button "Save Policy" in "policy" edit form
#    Then I wait for 3 seconds
#    Given rule "0" is "ALLOW" "machine" "all" where tags = "bla=bla"
#    Given rule "1" is "ALLOW" "cloud" "all" always
#    Given rule "2" is "DENY" "key" "edit" where id = "PolicyKey"
#    Then I logout
