@rbac-teams
Feature: Rbac

  team visibility how much time

  is it worth it

  @create-org
  Scenario: Owner creates a new organization
    Given rbac members are initialized
    Given I am logged in to mist.core
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

  @create-dup-org
  Scenario: Creating an org with the name used above, should bring a 409 error
    When I click the Gravatar
    And I wait for 1 seconds
    And I click the button "Add Organisation" in the user menu
    Then I expect the dialog "Add Organization" is open within 4 seconds
    And I wait for 1 seconds
    When I set the value "ORG_NAME" to field "Name" in "Add Organization" dialog
    And I click the "Add" button in the dialog "Add Organization"
    And I wait for 2 seconds
    Then there should be a "409" error message in "Add Organization" dialog

  @add-team
  Scenario: Owner creates a team
    When I visit the Teams page
    When I click the button "+"
    And I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Test Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    And "Test Team" team should be present within 5 seconds
    When I click the button "+"
    And I expect the dialog "Add Team" is open within 4 seconds
    When I set the value "Second Team" to field "Name" in "Add Team" dialog
    And I click the "Add" button in the dialog "Add Team"
    When I visit the Teams page
    And I refresh the page
    Then "Second Team" team should be present within 10 seconds

  @add-member2
   Scenario: Add member2
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
    When I visit the Teams page
    And I click the "Second team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I click the button "Invite Members" in "team" edit form
    And I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER2_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    And I click the button "Add" in "members" add form
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER2_EMAIL" should be pending
    Then I logout

   @member2-accepts-invitation
   Scenario: Add member2
    Then I should receive an email at the address "MEMBER2_EMAIL" with subject "[mist.io] Confirm your invitation" within 30 seconds
    And I follow the link inside the email
    Then I enter my rbac_member2 credentials for signup_password_set
    And I click the go button in the landing page popup
    And I wait for the links in homepage to appear
    Then I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    And "Second Team" team should be present within 5 seconds
    Then I logout

  @delete-members
  Scenario: Owner deletes team members
    Given I am logged in to mist.core as rbac_owner
    And I visit the Teams page
    And I wait for 3 seconds
    When I click the "Test Team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER2_EMAIL" should be confirmed
    When I delete user "MEMBER2_EMAIL" from team
    And I expect the dialog "Delete Member from Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Member from Team"
    And I expect the dialog "Delete Member from Team" is closed within 4 seconds
    When I delete user "MEMBER1_EMAIL" from team
    And I expect the dialog "Delete Member from Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Member from Team"
    And I expect the dialog "Delete Member from Team" is closed within 4 seconds

  @rename-team
  Scenario: Owner renames a team
    Given I am logged in to mist.core
    And I visit the Teams page
    And I wait for 3 seconds
    When I click the "TestTeam" "team"
    Then I click the button "Edit Team" in "team" edit form
    And I expect the dialog "Edit Team" is open within 4 seconds
    Then I expect the field "Name" in the dialog with title "Edit Team" to be visible within max 2 seconds
    When I set the value "Rbac Test Team" to field "Name" in "Edit Team" dialog
    And I change the visibility of the team inside the edit team dialog
    And I wait for 1 seconds
    And I click the "Submit" button in the dialog "Edit Team"
    And I expect the dialog "Edit Team" is closed within 4 seconds
    Then I visit the Home page
    Then I visit the Teams page
    And "Test Team" team should be absent within 5 seconds
    And "Rbac Test Team" team should be present within 5 seconds
    Then I logout

   @verify-delete-member
    Scenario: Member2 has been removed from org
    Given I am logged in to mist.core as rbac_member2
    When I visit the Teams page
    Then "Rbac Test Team" team should be absent within 5 seconds
    And "Test Team" team should be absent within 5 seconds
    Then I logout

  @delete-team
  Scenario: Owner deletes a team
    Given I am logged in to mist.core as rbac_owner
    When I visit the Teams page
    When I click the "Second Team" "team"
    And I expect the "team" edit form to be visible within max 5 seconds
    Then I click the button "Delete Team" from the menu of the "team" edit form
    And I expect the dialog "Delete Team" is open within 4 seconds
    And I click the "Delete" button in the dialog "Delete Team"
    Then I expect the dialog "Delete Team" is closed within 4 seconds
    Then I visit the Home page
    And I wait for 2 seconds
    And I visit the Teams page
    And "Second Team" team should be absent within 10 seconds
    Then I logout

  @verify-delete-member2
  Scenario: Mem2 needs to set an org
    Given I am logged in to mist.core as rbac_owner
    And I wait for the links in homepage to appear
    Then I should see the form to set name for new organization


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
