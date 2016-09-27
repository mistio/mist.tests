@images
Feature: Actions for Images

  # Not finished yet cause Image search is not working yet in polymist
  Scenario: Star image from Advanced search
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load
#    Given "AWS" cloud has been added
#    When I visit the Images page after the counter has loaded
#    And I wait for 3 seconds
#    Then there should be ticked Images in the list
#    When I search for "docker"
#    Then "Key1" key should be absent within 15 seconds
#    When I clear the search bar
#    Then "Key1" key should be present within 15 seconds
#    Then I visit the Home page
#    When I wait for the dashboard to load

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
