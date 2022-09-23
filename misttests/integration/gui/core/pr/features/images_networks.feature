@images-networks
Feature: Images-Networks

  Background:
    Given I am logged in to mist

  @image-search
  Scenario: Search image
    Given "DigitalOcean" cloud has been added
    Given "Amazon Web Services" cloud has been added
    Then I wait for the navigation menu to appear
    Then images counter should be greater than 12 within 80 seconds
    And I visit the Images page
    And I wait for 2 seconds
    And I search for "Ubuntu 20.04 (LTS) x64"
    Then "Ubuntu 20.04 (LTS) x64" image should be present within 15 seconds
    And "Debian 11 x64" image should be absent within 10 seconds
    When I clear the search bar
    Then "Debian 11 x64" image should be present within 5 seconds

  @image-star
  Scenario: Star image
    When I search for "Ubuntu 20.04 (LTS) x64"
    And I click the "Ubuntu 20.04 (LTS) x64" "image"
    Then I expect the "image" page to be visible within max 5 seconds
    When I wait for 1 seconds
    And I click the "Star" action button in the "image" page
    And  I visit the Home page
    And I refresh the page
    Then I wait for the navigation menu to appear
    When I visit the Images page
    And I wait for 2 seconds
    And I clear the search bar
    And I wait for 2 seconds
    And I search for "Ubuntu 20.04 (LTS) x64"
    Then the "Ubuntu 20.04 (LTS) x64" image should be "starred" within 20 seconds

  @image-unstar
  Scenario: Unstar image
    When I click the "Ubuntu 20.04 (LTS) x64" "image"
    Then I expect the "image" page to be visible within max 5 seconds
    When I click the "Unstar" action button in the "image" page
    And I clear the search bar
    And I wait for 2 seconds
    And  I visit the Home page
    And I wait for 2 seconds
    And I clear the search bar
    And I wait for 2 seconds
    And I visit the Images page
    And I wait for 2 seconds
    And I clear the search bar
    And I wait for 2 seconds
    And I search for "Ubuntu 20.04 (LTS) x64"
    Then the "Ubuntu 20.04 (LTS) x64" image should be "unstarred" within 20 seconds
    And I clear the search bar
    And I wait for 2 seconds

#  @image-tags
#  Scenario: Add tags to image
#    When I click the ""CoreOS-Beta" "image"
#    And I expect the "image" edit form to be visible within max 5 seconds
#    Then I click the button "Tags" in "image" edit form
#    And I expect for the tag popup to open within 4 seconds
#    When I remove all the previous tags
#    Then I add a tag with key "first" and value "tag"
#    Then I add a tag with key "second" and value "tag"
#    And I click the button "Save Tags" in the tag menu
#    Then I expect for the tag popup to close within 4 seconds
#    And I wait for 2 seconds
#    Then I ensure that the "image" has the tags "first:tag,second:tag"
#    Then I click the button "Tags" in "image" edit form
#    And I expect for the tag popup to open within 4 seconds
#    And I wait for 1 seconds
#    When I remove the tag with key "first"
#    And I wait for 1 seconds
#    And I click the button "Save Tags" in the tag menu
#    Then I expect for the tag popup to close within 4 seconds
#    And I ensure that the "image" has the tags "second:tag"

  @network-add
  Scenario: Add Network without specifying subnets
    When I visit the Networks page
    And I click the button "+"
    Then I expect the "network" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "network" add form
    And I wait for 1 seconds
    And I click the "Amazon Web Services" button in the "Select Cloud" dropdown in the "network" add form
    And I wait for 1 seconds
    And I set the value "network_random" to field "Name" in the "network" add form
    And I wait for 1 seconds
    And I set the value "10.146.0.0/20" to field "Network CIDR" in the "network" add form
    Then I expect for the button "Add" in the "network" add form to be clickable within 3 seconds
    When I focus on the button "Add" in the "network" add form
    And I click the button "Add" in the "network" add form
    Then I expect for "Networks" page to appear within max 10 seconds
    And "network_random" network should be present within 40 seconds
    When I click the "network_random" "network"
    And I expect the "network" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I should see a(n) "request" log entry of action "create_network" added "a few seconds ago" in the "network" page within 20 seconds
    Then there should be 0 subnets visible in single network page

  @network-delete
  Scenario: Delete Network
    When I click the "Delete" action button in the "network" page
    Then I expect the "Delete Network" dialog to be open within 4 seconds
    When I click the "Delete" button in the "Delete Network" dialog
    Then I expect the "Delete Network" dialog to be closed within 4 seconds
    When I visit the Home page
    And I visit the Networks page
    Then "network_random" network should be absent within 60 seconds

  @network-add-with-subnets
  Scenario: Add Network and  specify subnets
    When I click the button "+"
    Then I expect the "network" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "network" add form
    And I wait for 1 seconds
    And I click the "Amazon Web Services" button in the "Select Cloud" dropdown in the "network" add form
    And I wait for 1 seconds
    And I set the value "network_random" to field "Name" in the "network" add form
    And I wait for 1 seconds
    And I set the value "10.146.0.0/20" to field "Network CIDR" in the "network" add form
    And I click the "Create subnet" toggle button in the "network" add form
    Then I expect the field "Subnet CIDR" in the network add form to be visible within max 4 seconds
    When I set the value "10.146.0.0/20" to field "Subnet CIDR" in the "network" add form
    And I open the "Availability Zone" dropdown in the "network" add form
    And I wait for 1 seconds
    And I click the "ap-northeast-1a" button in the "Availability Zone" dropdown in the "network" add form
    And I focus on the button "Add" in the "network" add form
    And I click the button "Add" in the "network" add form
    Then I expect for "Networks" page to appear within max 30 seconds
    And "network_random" network should be present within 20 seconds
    And I wait for 1 seconds
    When I click the "network_random" "network"
    And I expect the "network" page to be visible within max 5 seconds
    And I refresh the page
    And I wait for 10 seconds
    Then there should be 1 subnets visible in single network page
    And the cidr of the subnet created should be "10.146.0.0/20"

  @network-delete
  Scenario: Delete Network from networks page
    When I visit the Networks page
    And I wait for 1 seconds
    And I select list item "network_random" network
    And I click the action "Delete" from the network list actions
    And I expect the "Delete Network" dialog to be open within 4 seconds
    And I wait for 2 seconds
    And I click the "Delete" button in the "Delete Network" dialog
    And I expect the "Delete Network" dialog to be closed within 4 seconds
    Then "network_random" network should be absent within 60 seconds
