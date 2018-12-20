@rbac-rules-1
Feature: RBAC-rules-v1

  @create-users-org-team
  Scenario: Owner creates a new organization,invites member1 and adds a Softlayer cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist
    And I visit the Home page
    Then I expect for "addBtn" to be clickable within max 20 seconds
    Given cloud "Docker" has been added via API request

  @allow-read-cloud
   Scenario: Allow reading a cloud
    When I have given card details if needed
    When I visit the Teams page
    And I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds

  @allow-read-script
  Scenario: Allow reading a script and add a script
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "script" "read"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    Given script "TestScript" is added via API request
    Then I logout

  @member1-view-cloud-success
  Scenario: Verify that member1 can view a cloud
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 1 clouds added

  @member1-add-cloud-fail
  Scenario: Member1 cannot add cloud
    When I click the "new cloud" button with id "addBtn"
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "Packet" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "Packet" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    And I click the button "Add Cloud" in "cloud" add form
    And I wait for 1 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then I should have 1 clouds added

  @member1-view-script-success
  Scenario: Member 1 should be able to view the script
    When I visit the Scripts page
    And I wait for 2 seconds
    Then I click the "TestScript" "script"
    And I expect the "script" edit form to be visible within max 5 seconds
    Then I logout

  @allow-add-cloud
  Scenario: Allow adding a cloud
    Given I am logged in to mist as rbac_owner
    And I visit the Teams page
    When I click the "Test team" "team"
    Then I expect the "team" edit form to be visible within max 5 seconds
    When I focus on the button "Add a new rule" in "policy" edit form
    And I click the button "Add a new rule" in "policy" edit form
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "cloud" "add"
    And I click the button "Save Policy" in "policy" edit form
    And I wait for 1 seconds
    Then I logout

  @member1-add-cloud-success
  Scenario: Member 1 should now be able to add cloud
    Given I am logged in to mist as rbac_member1
    When I click the "new cloud" button with id "addBtn"
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "Packet" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "Packet" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    And I click the button "Add Cloud" in "cloud" add form
    And I wait for 2 seconds
    And I visit the Home page
    And I wait for the dashboard to load
    Then the "Packet" provider should be added within 120 seconds
    And I should have 2 clouds added

  @member1-delete-cloud-fail
  Scenario: Member 1 should not be able to delete cloud
    When I wait for 1 seconds
    And I open the cloud menu for "Packet"
    Then I expect the "cloud" edit form to be visible within max 10 seconds
    When I click the button "Delete" in the "cloud" page actions menu
    Then I expect the dialog "Delete Packet" is open within 4 seconds
    And I wait for 2 seconds
    And I focus on the button "Delete" in "cloud" edit form
    And I click the button "Delete" in "cloud" edit form
    And I wait for 3 seconds
    And I visit the Home page
    # deletion did not work
    Then I should have 2 clouds added
