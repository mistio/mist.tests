@clouds-add-2
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core
    Then I expect for "addBtn" to be clickable within max 20 seconds

  @cloud-add
  Scenario Outline: Add cloud for multiple providers
    When I click the "new cloud" button with id "addBtn"
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "<provider>" provider
    And I wait for 3 seconds
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "<provider>" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    And I click the button "Add Cloud" in "cloud" add form
    And I wait for the links in homepage to appear
    And I scroll the clouds list into view
    Then the "<provider>" provider should be added within 120 seconds


    Examples: Providers
    | provider       |
    | Linode         |
    | AWS            |

  @cloud-edit-creds
  Scenario: AWS cloud added in the beginning, does not have access to list images (DenyDescribeImages policy in aws), whereas the seconds one has (EC2FullAccess)
    When I visit the Images page
    And I search for "CoreOS"
    Then "CoreOS stable 1068.8.0 (PV)" image should be absent within 10 seconds
    Then I visit the Home page
    And I wait for the dashboard to load
    When I open the cloud menu for "AWS"
    Then I expect the "cloud" edit form to be visible within max 10 seconds
    When I click the button "Edit Credentials" in the "cloud" page actions menu
    Then I expect the dialog "Edit Credentials" is open within 4 seconds
    When I use my second AWS credentials
    And I wait for 1 seconds
    And I focus on the button "Edit Credentials" in "cloud" edit form
    And I click the button "Edit Credentials" in "cloud" edit form
    And I wait for 3 seconds
    And I visit the Images page
    And I search for "CoreOS"
    Then "CoreOS stable 1068.8.0 (PV)" image should be present within 20 seconds
