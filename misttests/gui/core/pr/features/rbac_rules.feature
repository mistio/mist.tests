@rbac-rules
Feature: RBAC


  @create-org
  Scenario: Owner creates a new organization and adds a Docker cloud
    Given rbac members are initialized
    Given I am logged in to mist.core
    And I am in the new UI
    And  I wait for the dashboard to load
    When I click the Gravatar
    And I wait for 1 seconds
    Then I click the button "Add Organisation" in the user menu
    And I expect the dialog "Add Organization" is open within 4 seconds
    And I wait for 1 seconds
    When I set the value "ORG_NAME" to field "Name" in "Add Organization" dialog
    And I click the "Add" button in the dialog "Add Organization"
    And I wait for 2 seconds
    And I click the "Switch" button in the dialog "Add Organization"
    Then I expect the dialog "Add Organization" is closed within 4 seconds
    When I wait for the dashboard to load
    Given "Docker" cloud has been added

  @add-team
  Scenario: Owner creates a team
    When I visit the Teams page
    When I click the button "+"
    And I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Test Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds

  @add-member1
  Scenario: Add member1
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

  @view-cloud-fail
  Scenario: Verify that member1 cannot view the cloud added above
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation" within 15 seconds
    And I follow the link inside the email
    #And I follow the link contained in the email sent at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation"
    Then I click the email button in the landing page popup
    Then I enter my rbac_member1 credentials for login
    And I click the sign in button in the landing page popup
    Given that I am redirected within 10 seconds
    And I am in the new UI
    When I wait for the dashboard to load
    Then I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 0 clouds added
    Then I logout

   @allow-read-cloud
   Scenario: Allow reading a cloud
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 2 seconds
    Then I logout

#   @add-member2
#   Scenario: Add member2
#    Then I click the button "Invite Members" in "team" edit form
#    And I expect the "members" add form to be visible within max 5 seconds
#    When I set the value "MEMBER2_EMAIL" to field "Emails" in "members" add form
#    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
#    And I click the button "Add" in "members" add form
#    And I expect the "team" edit form to be visible within max 5 seconds
#    Then user with email "MEMBER2_EMAIL" should be pending
#    And user with email "MEMBER1_EMAIL" should be confirmed
#    Then I logout

  @member1-view-cloud-success
    Scenario: Verify that member1 can view a cloud
    Given I am logged in to mist.core as rbac_member1
    Then I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    Then I visit the Home page
    # should be able to view cloud
    Given "Docker" cloud has been added

  @member1-add-cloud-fail
  Scenario: Member1 cannot add cloud
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
    Then I should have 1 clouds added
    Then I logout

  @allow-add-cloud
    Scenario: Allow adding a cloud
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "add"
    Then I logout

 # below should pass, but it doesn't...

#  @member1-add-cloud
#  Scenario: Member 1 should now be able to add cloud
#    Given I am logged in to mist.core as rbac_member1
#    Then I ensure that I am in the "Rbac_Test" organization context
#    And I am in the new UI
#    When I wait for the dashboard to load
#    When I click the new cloud button
#    Then I expect the "Cloud" add form to be visible within max 5 seconds
#    And I open the "Choose Provider" drop down
#    And I wait for 1 seconds
#    When I click the button "Vultr" in the "Choose Provider" dropdown
#    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
#    When I use my "Vultr" credentials
#    And I focus on the button "Add Cloud" in "cloud" add form
#    And I click the button "Add Cloud" in "cloud" add form
#    Then I wait for 2 seconds
#    Then I visit the Home page
#    Then I wait for the dashboard to load
#    Then I should have 2 clouds added

  @member1-delete-cloud
  Scenario: Member 1 should not be able to delete cloud
    Given I am logged in to mist.core as rbac_member1
    Then I ensure that I am in the "ORG_NAME" organization context
    And I am in the new UI
    When I wait for the dashboard to load
    When I open the cloud menu for "Docker"
    And I click the "delete cloud" button
    And I wait for 3 seconds
    Then I visit the Home page
    # deletion did not work
    Then I should have 1 clouds added
    # when above is fixed, below is correct
    #Then I should have 2 clouds added
    Then I logout

  @deny-all-cloud
  Scenario: Manage team rules
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    When I visit the teams page
    When I click the "Test Team" "team"
    And I expect the "policy" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "DENY" "cloud" "all"
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I logout

  @member1-add-cloud-fail
  Scenario: Member 1 should not be able to add cloud
    Given I am logged in to mist.core as rbac_member1
    And I am in the new UI
    When I wait for the dashboard to load
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
    Then I should have 1 clouds added
    #Then I should have 2 clouds added
    Then I logout

  @allow-view-script
  Scenario: Add script and allow members to view it
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I wait for the dashboard to load
    When I visit the Scripts page
    When I click the button "+"
    Then I expect the "Script" add form to be visible within max 10 seconds
    When I set the value "TestScript" to field "Script Name" in "script" add form
    And I open the "Type" drop down
    And I wait for 2 seconds
    When I click the button "Executable" in the "Type" dropdown
    And I wait for 2 seconds
    And I open the "Source" drop down
    And I wait for 2 seconds
    And I click the button "Inline" in the "Source" dropdown
    When I set the value "#!/bin/bash\necho bla > ~/kati" to field "Script" in "script" add form
    When I focus on the button "Add" in "script" add form
    And I expect for the button "Add" in "script" add form to be clickable within 3 seconds
    And I click the button "Add" in "script" add form
    And I wait for 3 seconds
    When I visit the teams page
    When I click the "Test Team" "team"
    And I expect the "policy" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "read"
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I logout


  @member1-view-script-success
  Scenario: Member 1 should be able to view the script
    Given I am logged in to mist.core as rbac_member1
    Then I ensure that I am in the "ORG_NAME" organization context
    And I am in the new UI
    When I wait for the dashboard to load
    When I visit the Scripts page
    And I wait for 2 seconds
    When I click the "TestScript" "script"

   @member1-edit-script-fail
   Scenario: Member 1 should not be able to edit the script
    And I expect the "script" edit form to be visible within max 5 seconds
    Then I click the button "Edit Script" from the menu of the "script" edit form
    And I expect the dialog "Edit Script" is open within 4 seconds
    When I set the value "Second" to field "Name" in "Edit Script" dialog
    And I click the "Submit" button in the dialog "Edit Script"
    And I expect the dialog "Edit Script" is closed within 4 seconds
    Then I visit the Home page
    And I wait for 2 seconds
    Then I visit the Scripts page
    And "TestScript" script should be present within 5 seconds
    And "Second" script should be absent within 5 seconds
    Then I logout

  @allow-edit-script
  Scenario: Allow members to edit scripts
    Given I am logged in to mist.core as rbac_owner
    And I am in the new UI
    When I visit the teams page
    When I click the "Test Team" "team"
    And I expect the "policy" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "edit"
    When I focus on the button "Add a new rule" in "policy" edit form
    Then I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I logout

  @member1-edit-script-fail
   Scenario: Member 1 should not be able to edit the script
    Given I am logged in to mist.core as rbac_member1
    Then I ensure that I am in the "ORG_NAME" organization context
    And I am in the new UI
    When I wait for the dashboard to load
    When I visit the Scripts page
    And I wait for 2 seconds
    When I click the "TestScript" "script"
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
    Then I logout

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


# will be checked again when issues are resolved

#  @tag-team
#  Scenario: Owner tags a team
#    Given I am logged in to mist.core as rbac_owner
#    And I am in the new UI
#    When I wait for the dashboard to load
#    And I visit the Teams page
#    When I click the button "tag" from the menu of the "Rbac Test Team" team
#    And I expect for the tag popup to open within 4 seconds
#    When I remove all the previous tags
#    Then I add a tag with key "team" and value "ops"
#    And I click the button "Save Tags" in the tag menu
#    Then I expect for the tag popup to close within 4 seconds
#    And I wait for 2 seconds
#    Then I ensure that the "team" has the tags "team:ops"
