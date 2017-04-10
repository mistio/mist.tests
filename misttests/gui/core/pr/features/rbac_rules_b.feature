# Created by spiros at 10/4/2017
Feature: RBAC


  @create-users-org-team
  Scenario: Owner creates a new organization and adds a Softlayer cloud
    Given rbac members, organization and team are initialized
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds
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
    And I wait for the links in homepage to appear
    When I ensure that I am in the "ORG_NAME" organization context
    And I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    When I visit the Home page
    Then I should have 0 clouds added
    And I logout