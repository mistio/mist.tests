@user-init
Feature: Login Scenarios

  @signup
  Scenario: Sign Up success
    Given I am not logged in to mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    Then I save the confirmation link and delete the email
    Then I refresh the browser
    Given I am not logged in to mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Confirm your registration" within 10 seconds
    When I make sure that this link is the same as before at email address "EMAIL"
    And I follow the link contained in the email sent at the address "EMAIL" with subject "[mist.io] Confirm your registration"
    Then I enter my standard credentials for signup_password_set
    And I click the submit button in the landing page popup
    And I wait for the mist.io splash page to load
    Then I logout
    Given I am not logged in to mist.core
    When I open the signup popup
    Then I click the sign up button in the landing page popup
    Then I click the email button in the landing page popup
    And I enter my standard credentials for signup
    And I click the sign up button in the landing page popup
    Then I should get an already registered error
    Then I close the "Register" popup
    And I wait for 2 seconds

  @forgot-password
  Scenario: Forgot password
    When I visit mist.core
    When I open the login popup
    Then I click the email button in the landing page popup
    And I click the forgot password button in the landing page popup
    And I enter my standard credentials for password_reset_request
    And I click the reset_password_email_submit button in the landing page popup
    Then I should receive an email at the address "EMAIL" with subject "[mist.io] Password reset request" within 10 seconds
    And I follow the link contained in the email sent at the address "EMAIL" with subject "[mist.io] Password reset request"
    And I enter my standard credentials for password_reset
    Then I click the reset_pass_submit button in the landing page popup
    And I wait for the mist.io splash page to load
    And I logout

  @check-redirect
  Scenario: Add EC2 cloud, go to Machines logout and check redirect
    Given I am logged in to mist.core
    Given "EC2" cloud has been added
    Then I logout
    And I visit the machines page with a url
    When I wait for 2 seconds
    Then I click the email button in the landing page popup
    When I enter my standard credentials for login
    And I click the sign in button in the landing page popup
    Then I wait for the mist.io splash page to load
    And I should be in the machines page
    Then I logout

#  @multiple-login
#  Scenario: Launch two browsers and try to login from both
#    Given I am logged in to mist.core
#    When I launch a second browser
#    And I switch browser
#    When I visit mist.core
#    Given I am logged in to mist.core
#    When I visit the Account page
#    Then I wait for the mist.io splash page to load
#    When I focus on the "Create Token" button
#    And I revoke all sessions
#    Then I wait for 2 seconds
#    When I switch browser
#    And I refresh the current page
#    Then I should see the landing page within 10 seconds
#    Then I switch browser
#    When I focus on the "Home" button
#    Then I logout
#    And I quit the second browser
