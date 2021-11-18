@constraints-expiration
Feature: Contstraints-RBAC-rules

  @create-users-org-team
  Scenario: Owner creates a new organization,invites member1 and adds a Docker cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist
    And I visit the Home page
    Given "Docker" cloud has been added
    And key "DummyKey" has been added via API request

  @set-up-constraints
  Scenario: Owner adds rule with size and field constraints on machine create
    When I visit the Teams page
    And I wait for 1 seconds
    And I click the "Test team" "team"
    Then I expect the "team" page to be visible within max 5 seconds
    And I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "machine" "create" with "expiration" constraints
    And I wait for 1 seconds
    And I click the button "Add a new rule" in the "team" page
    And I wait for 1 seconds
    Then I add the rule always "ALLOW" "all" "all"
    And I click the button "Save Policy" in the "team" page
    And I wait for 1 seconds
    Then I logout

  @check-constraints-result
  Scenario: Create a machine and if it expires and if notification arrives
    Given I am logged in to mist as rbac_member1
    And I wait for the navigation menu to appear
    And I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Docker" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    When I select the proper values for "Docker" to create the "ui-test-expiration-random" machine
    And I wait for 3 seconds
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    And I wait for 20 seconds
    When I visit the Machines page
    And I wait for 5 seconds
    And I search for "ui-test-expiration-random"
    Then "ui-test-expiration-random" machine state has to be "running" within 100 seconds
    And I wait for 5 seconds
    When I visit the Home page
    And I wait for 1 seconds
    Then I should see a(n) "job" log entry of action "post_deploy_finished" added "a few seconds ago" in the "dashboard" page within 100 seconds
    When I visit the Machines page
    And I wait for 2 seconds
    When I click the "ui-test-expiration-random" "machine"
    And I wait for 3 seconds
    Then I expect to see "in x minutes" in the expiration section of the machine page
    When I click the "edit expiration" button in the "machine" page
    Then I expect the "Edit expiration date" dialog to be open within 7 seconds
    And I set the expiration to "2" "minutes" in the expiration dialog
    And I wait for 3 seconds
    And I click the "Save" button in the "Edit expiration date" dialog
    And I wait for 10 seconds
    When I visit the Home page
    And I wait for 105 seconds
    Then I should see a(n) "observation" log entry of action "destroy_machine" added "a few seconds ago" in the "dashboard" page within 60 seconds
    And I should receive an email at the address "MEMBER1_EMAIL" with subject "Machine is about to expire" within 60 seconds
