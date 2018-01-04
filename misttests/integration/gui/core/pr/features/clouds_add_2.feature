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
    | OpenStack      |
    | Docker         |
