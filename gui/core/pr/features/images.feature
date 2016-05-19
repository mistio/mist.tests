@images
Feature: Actions for Images

  Background:
    When I setup user with email "EMAIL"

  Scenario: Star image from Advanced search
    Given I am logged in to mist.core
    Given "EC2" cloud has been added
    When I visit the Images page after the counter has loaded
    Then there should be starred Images
    When I search for the "bitnami" Image
    And I click the button "Load more"
    Then the images list should be loaded within 100 seconds
    When I star an image that contains "bitnami"
    And I clear the Images search bar
    Then the images list should be loaded within 100 seconds
    When I scroll down until all starred images appear
    Then an image that contains "the_image_name_i_starred" should be starred
    When I focus on the "the_image_name_i_starred" button
    Then I unstar the image that contains "the_image_name_i_starred"
