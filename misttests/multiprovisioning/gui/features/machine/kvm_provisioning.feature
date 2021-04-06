@kvm-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear

  @kvm-machine-create
  Scenario: Create a machine in KVM provider, with default size(256mb RAM, 1 cpu)
    When I add the key needed for Other Server
    And I visit the Home page
    And I click the fab button in the "dashboard" page
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "KVM" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "KVM" credentials
    And I focus on the button "Add Cloud" in the "cloud" add form
    Then I click the button "Add Cloud" in the "cloud" add form
    And I wait for 180 seconds
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "KVM" provider should be added within 30 seconds
    And I wait for 60 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "KVM" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "kvm-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "bionic-server-cloudimg-amd64.img" button in the "Image" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 5 seconds
    And I click the "KVMKey" button in the "Key" dropdown in the "machine" add form
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine should be present within 120 seconds

  @kvm-machine-destroy
  Scenario: Destroy a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine should be present within 10 seconds
    When I click the "kvm-mp-test-random" "machine"
    And I wait for 1 seconds
    Then I expect the "machine" page to be visible within max 5 seconds
    And I click the "Destroy" action button in the "machine" page
    Then I expect the "Destroy Machine" dialog to be open within 4 seconds
    When I click the "Destroy" button in the "Destroy Machine" dialog
    And I refresh the page
    And I wait for 30 seconds
    Then I should see a(n) "request" log entry of action "destroy_machine" added "a few seconds ago" in the "machine" page within 100 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    And I refresh the page
    Then "kvm-mp-test-random" machine state has to be "terminated" within 300 seconds

  @kvm-machine-rename
  Scenario: Rename a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine should be present within 10 seconds
    When I click the "kvm-mp-test-random" "machine"
    And I wait for 1 seconds
    Then I expect the "machine" page to be visible within max 5 seconds
    When I click the "Rename" action button in the "machine" page
    Then I expect the "Rename Machine" dialog to be open within 4 seconds
    When I set the value "kvm-mp-test-random-renamed" to field "kvm-mp-test-random" in the "Rename Machine" dialog
    And I wait for 1 seconds
    And I click the "Submit" button in the "Rename Machine" dialog
    Then I expect the "Rename Machine" dialog to be closed within 4 seconds
    And I wait for 60 seconds
    And I visit the Machines page
    And I clear the search bar
    And I search for "kvm-mp-test-random-renamed"
    Then "kvm-mp-test-random-renamed" machine should be present within 300 seconds
