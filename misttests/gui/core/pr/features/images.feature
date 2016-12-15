@images
Feature: Images

  Background:
    Given I am logged in to mist.core
    And I am in the new UI

  @image-search
  Scenario: Star image from Advanced search
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


#   Then there should be ticked Images in the list

#    When I search for the "docker" Image
#    And I click the button "Load more"
#    Then the images list should be loaded within 100 seconds
#    When I star an image that contains "docker"
#    And I clear the Images search bar
#    Then the images list should be loaded within 100 seconds
#    When I scroll down until all starred images appear
#    Then an image that contains "the_image_name_i_starred" should be starred
#    When I focus on the "the_image_name_i_starred" button
#    Then I unstar the image that contains "the_image_name_i_starred"
