@constraints-field-size
Feature: Constraints-field-size

  @create-users-org-team
  Scenario: Owner creates a new organization,invites member1 and adds a VSphere cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist
    And I visit the Home page
    Given "vmware vsphere" cloud has been added

  @set-up-constraints
  Scenario: Owner adds rule with size and field constraints on machine create
    When I visit the Teams page
    And I wait for 1 seconds
    And I click the "Test team" "team"
    Then I expect the "team" page to be visible within max 5 seconds
    And I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "machine" "create" with "kevin's" constraints
    And I wait for 1 seconds
    And I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in the "team" page
    And I wait for 1 seconds
    Then I logout

  @check-constraints-result
  Scenario: Check if datastore and size are absent from machine create from
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "VMware vSphere" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I expect the "Datastore" dropdown to be absent in the "machine" add form
    And I expect the "disk" slider of the size field to be absent in the "machine" add form
    