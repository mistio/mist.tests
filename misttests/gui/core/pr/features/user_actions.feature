@user-actions
Feature: Login Scenarios and Api Token

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
    And "Second Team" team should be present within 5 seconds

  @add-member1
  Scenario: Add member1
    When I visit the Home page
    When I refresh the page
    And I wait for the links in homepage to appear
    And I visit the Teams page
    When I click the "Test team" "team"
    And I expect the "team" edit form to be visible within max 8 seconds
    Then I click the button "Invite Members" in "team" edit form
    And I expect the "members" add form to be visible within max 5 seconds
    When I set the value "MEMBER1_EMAIL" to field "Emails" in "members" add form
    Then I expect for the button "Add" in "members" add form to be clickable within 2 seconds
    And I click the button "Add" in "members" add form
    And I expect the "team" edit form to be visible within max 5 seconds
    Then user with email "MEMBER1_EMAIL" should be pending
    Then I logout
    Then I should receive an email at the address "MEMBER1_EMAIL" with subject "[mist.io] Confirm your invitation" within 30 seconds
    And I follow the link inside the email
    Then I enter my rbac_member1 credentials for login
    And I click the sign in button in the landing page popup
    Given that I am redirected within 5 seconds
    And I wait for the links in homepage to appear
    Then I ensure that I am in the "ORG_NAME" organization context
    When I visit the Teams page
    Then "Test Team" team should be present within 5 seconds
    Then I logout

  @api-token-test
  Scenario: Create api token and test it with API call
    Given I am logged in to mist.core
    When I visit the Account page
    And I wait for 3 seconds
    Then I click the "API Tokens" button with id "API Tokens"
    # below needs to be fixed in the backend
    # When I revoke all api tokens
    Then I click the "Create API Token" button with id "Create API Token"
    # create a step that checks if popup with id is open
    # And I expect for "createTokenDialog" popup to appear within max 4 seconds
    And I wait for 2 seconds
    Then I type "Test token" in input with id "tokenName"
    And I wait for 1 seconds
    Then I click the button "Never" from the ttl dropdown
    And I wait for 1 seconds
    Then I type "PASSWORD1" in input with id "pass"
    And I wait for 1 seconds
    And I click the "Create" button with id "Create"
    And I wait for 5 seconds
    When I get the new api token value "BLABLA_TOKEN"
    Then I test the api token "BLABLA_TOKEN". It should work.
    #When i revoke it, it should fail #needs to be fixed in the backend
    #Then I test the api token "BLABLA_TOKEN". It should fail.

  @signup
  Scenario: Sign Up success
    When I make sure user with email "EMAIL" is absent
    Given I am not logged in to mist.core
    When I open the signup popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 30 seconds
    When I follow the link inside the email
    And I delete old emails
    And I enter my standard credentials for signup_password_set
    And I click the go button in the landing page popup
    Then I wait for the links in homepage to appear
    And I logout
    Given I am not logged in to mist.core
    When I open the signup popup
    And I wait for 3 seconds
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    And I wait for 3 seconds
    Then I should get a conflict error

  @invalid-credentials
  Scenario: 'Unauthorized' message should appear
    When I visit mist.core
    And I open the login popup
    And I wait for 3 seconds
    And I enter my alt credentials for login
    And I click the sign in button in the landing page popup
    And I wait for 3 seconds
    Then there should be an "Unauthorized" error message inside the "sign in" button

  @invalid-email
  Scenario: Sign in button should not become clickable
    When I wait for 1 seconds
    And I enter my invalid_email credentials for login
    Then the sign in button should be not clickable

  @forgot-password
  Scenario: Forgot password
    When I visit mist.core
    And I open the login popup
    And I wait for 3 seconds
    And I click the forgot password button in the landing page popup
    And I wait for 3 seconds
    And I enter my standard credentials for password_reset_request
    And I click the reset_password_email_submit button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Password reset request" within 30 seconds
    When I follow the link inside the email
    And I enter my new_creds credentials for password_reset
    And I click the reset_pass_submit button in the landing page popup
    And I wait for the links in homepage to appear
    And I logout
    And I open the login popup
    And I enter my new_creds credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the links in homepage to appear
