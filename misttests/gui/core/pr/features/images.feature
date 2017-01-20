@images
Feature: Images

  Background:
    Given I am logged in to mist.core
    And I am in the new UI

  @image-search
  Scenario: Search image
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

  @image-star
    When I click the "CoreOS-Beta" "image"
    And I expect the "image" edit form to be visible within max 5 seconds
    Then I click the button "Unstar" in "image" edit form
    When I visit the Images page
    # then CoreOS-Beta image should be unstarred within 10 seconds
    When I click the "CoreOS-Beta" "image"
    And I expect the "image" edit form to be visible within max 5 seconds
    Then I click the button "Unstar" in "image" edit form
    When I visit the Images page
    # then CoreOS-Beta image should be starred within 10 seconds

    When I star an image that contains "openstack"
#    Then I unstar the image that contains "the_image_name_i_starred"

#    And I clear the Images search bar
#    Then the images list should be loaded within 100 seconds
#    When I scroll down until all starred images appear
#    Then an image that contains "the_image_name_i_starred" should be starred
#    When I focus on the "the_image_name_i_starred" button
    #Then I unstar the image that contains "the_image_name_i_starred"
