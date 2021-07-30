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
    Then I expect the field "Name" in the cloud add form to be visible within max 4 seconds
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
    And I click the "cirros-0.5.1-x86_64-disk.img" button in the "Image" dropdown in the "machine" add form
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
    And I refresh the page
    Then I should see a(n) "request" log entry of action "destroy_machine" added "a few seconds ago" in the "machine" page within 100 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    And I refresh the page
    Then "kvm-mp-test-random" machine state has to be "terminated" within 300 seconds

  @kvm-machine-clone
  Scenario: Clone a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine should be present within 10 seconds
    When I click the "kvm-mp-test-random" "machine"
    And I wait for 1 seconds
    Then I expect the "machine" page to be visible within max 5 seconds
    And I click the "Clone" action button in the "machine" page
    Then I expect the "Clone Machine" dialog to be open within 4 seconds
    When I set the value "temp-kvm-machine" to field "Clone's Name" in the "Clone Machine" dialog
    And I wait for 1 seconds
    When I click the "Clone" button in the "Clone Machine" dialog
    And I refresh the page
    Then I wait for 30 seconds
    And I refresh the page
    Then I should see a(n) "request" log entry of action "clone_machine" added "a few seconds ago" in the "machine" page within 100 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "temp-kvm-machine"
    And I refresh the page
    Then "temp-kvm-machine" machine state has to be "running" within 300 seconds

  @kvm-machine-rename
  Scenario: Rename a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "temp-kvm-machine"
    Then "temp-kvm-machine" machine should be present within 10 seconds
    When I click the "temp-kvm-machine" "machine"
    And I wait for 1 seconds
    Then I expect the "machine" page to be visible within max 5 seconds
    And I click the "Destroy" action button in the "machine" page
    Then I expect the "Destroy Machine" dialog to be open within 4 seconds
    When I click the "Destroy" button in the "Destroy Machine" dialog
    And I refresh the page
    And I wait for 30 seconds
    And I refresh the page
    And I click the "Rename" action button in the "machine" page
    Then I expect the "Rename Machine" dialog to be open within 4 seconds
    When I set the value "temp-kvm-machine-renamed" to field "temp-kvm-machine" in the "Rename Machine" dialog
    And I wait for 1 seconds
    And I click the "Submit" button in the "Rename Machine" dialog
    And I wait for 60 seconds
    And I visit the Machines page
    And I clear the search bar
    And I search for "temp-kvm-machine-renamed"
    Then "temp-kvm-machine-renamed" machine should be present within 300 seconds

  @kvm-machine-undefine
  Scenario: Undefine a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "temp-kvm-machine-renamed"
    Then "temp-kvm-machine-renamed" machine should be present within 10 seconds
    When I click the "temp-kvm-machine-renamed" "machine"
    And I wait for 1 seconds
    When I click the "Undefine" action button in the "machine" page
    Then I expect the "Undefine Machine" dialog to be open within 4 seconds
    When I click the "Undefine" button in the "Undefine Machine" dialog
    And I refresh the page
    And I wait for 30 seconds
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "temp-kvm-machine-renamed"
    And I refresh the page
    Then "temp-kvm-machine-renamed" machine should be absent within 3 seconds

  @kvm-machine-start
  Scenario: Start a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine should be present within 10 seconds
    When I click the "kvm-mp-test-random" "machine"
    And I wait for 1 seconds
    Then I expect the "machine" page to be visible within max 5 seconds
    And I click the "Start" action button in the "machine" page
    Then I expect the "Start Machine" dialog to be open within 4 seconds
    When I click the "Start" button in the "Start Machine" dialog
    And I wait for 30 seconds
    Then I should see a(n) "request" log entry of action "start_machine" added "a few seconds ago" in the "machine" page within 100 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine state has to be "running" within 300 seconds

  @kvm-machine-stop
  Scenario: Stop a KVM machine
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine should be present within 10 seconds
    When I click the "kvm-mp-test-random" "machine"
    And I wait for 1 seconds
    Then I expect the "machine" page to be visible within max 5 seconds
    When I wait for 180 seconds
    And I click the "Stop" action button in the "machine" page
    Then I expect the "Stop Machine" dialog to be open within 4 seconds
    And I click the "Stop" button in the "Stop Machine" dialog
    And I wait for 30 seconds
    Then I should see a(n) "request" log entry of action "stop_machine" added "a few seconds ago" in the "machine" page within 100 seconds
    And I wait for 120 seconds
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "kvm-mp-test-random"
    Then "kvm-mp-test-random" machine state has to be "terminated" within 300 seconds
