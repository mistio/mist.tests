@sso
Feature: SSO Login


    Background:

        When I visit mist.core
        Given I am not logged in to mist.core


    Scenario: Register with Google

        Given There is no user in the db with email "tester.mist.io@gmail.com"
        When I click the "TRY NOW FOR FREE" button in the splash page
        When I click the button "Sign up with Google"
        And I wait for 5 seconds
        Then I do the Google login
        Then I logout

    Scenario: Register with Github

        Given There is no user in the db with email "tester.mist.io@gmail.com"
        When I click the "TRY NOW FOR FREE" button in the splash page
        When I click the button "Sign up with Github"
        And I wait for 5 seconds
        Then I do the Github login
        Then I logout

    Scenario: Register while registered with Google

        Given There is a user in the db with email "tester.mist.io@gmail.com"
        When I click the "TRY NOW FOR FREE" button in the splash page
        When I click the button "Sign up with Google"
        Then I wait for 3 seconds
        Then I do the Google login
        Then I logout

    Scenario: Register while registered with Github

        Given There is a user in the db with email "tester.mist.io@gmail.com"
        When I click the "TRY NOW FOR FREE" button in the splash page
        When I click the button "Sign up with Github"
        Then I wait for 3 seconds
        Then I do the Github login
        Then I logout

    Scenario: Login while not registered with Google

        Given There is no user in the db with email "tester.mist.io@gmail.com"
        When I click the "SIGN IN" button in the splash page
        When I click the button "Sign in with Google"
        And I wait for 3 seconds
        Then I do the Google login
        Then I logout

    Scenario: Login while not registered with Github

        Given There is no user in the db with email "tester.mist.io@gmail.com"
        When I click the "SIGN IN" button in the splash page
        When I click the button "Sign in with Github"
        And I wait for 3 seconds
        Then I do the Github login
        Then I logout

    Scenario: Login with Google

        Given There is a user in the db with email "tester.mist.io@gmail.com"
        When I click the "SIGN IN" button in the splash page
        When I click the button "Sign in with Google"
        And I wait for 3 seconds
        Then I do the Google login
        Then I logout

    Scenario: Login with Github

        Given There is a user in the db with email "tester.mist.io@gmail.com"
        When I click the "SIGN IN" button in the splash page
        When I click the button "Sign in with Github"
        And I wait for 3 seconds
        Then I do the Github login
        Then I logout
