@images
Feature: Images

  @image-search
  Scenario: Search image
    Given I am logged in to mist.core
    When I wait for the dashboard to load
    Given "OpenStack" cloud has been added
    When I visit the Images page
    When I search for "CoreOS"
    Then "CoreOS-Alpha" image should be present within 3 seconds
    And "CoreOS-Beta" image should be present within 3 seconds
    When I search for "CoreOS-Alpha"
    Then "CoreOS-Alpha" image should be present within 3 seconds
    And "CoreOS-Beta" image should be absent within 3 seconds
    When I clear the search bar
    Then "CoreOS-Beta" image should be present within 5 seconds

  @image-unstar
  Scenario: Unstar image
    When I click the "CoreOS-Beta" "image"
    And I expect the "image" edit form to be visible within max 5 seconds
    Then I click the button "Unstar" in "image" edit form
    When I visit the Images page
    Then the "CoreOS-Beta" image should be "unstarred" within 10 seconds

  @image-unstar
  Scenario: Star image
    When I click the "CoreOS-Beta" "image"
    And I expect the "image" edit form to be visible within max 5 seconds
    Then I click the button "Star" in "image" edit form
    When I visit the Images page
    # then CoreOS-Beta image should be starred within 10 seconds
