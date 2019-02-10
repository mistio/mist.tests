@clouds-add-1
Feature: Add second-tier clouds

  Background:
    Given I am logged in to mist

  @cloud-add
  Scenario Outline: Add cloud for multiple providers
    When I click the fab button in the "dashboard" page
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "<provider>" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "<provider>" credentials
    And I focus on the button "Add Cloud" in the "cloud" add form
    And I click the button "Add Cloud" in the "cloud" add form
    And I wait for the navigation menu to appear
    And I scroll the clouds list into view
    Then the "<provider>" provider should be added within 120 seconds


    Examples: Providers
    | provider       |
    | Azure ARM      |
#    | Vultr         |
#    | AWS            |
#    | Packet	     |
#    | Vmware         |
#    | HostVirtual    |

  @other-server-add
  Scenario: Add other-server
    When I refresh the page
    When I add the key needed for Other Server
    When I click the fab button in the "dashboard" page
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "Other Server" provider
    Then I expect the field "Cloud Title" in the cloud add form to be visible within max 4 seconds
    When I use my "Other Server" credentials
    And I focus on the button "Add Cloud" in the "cloud" add form
    Then I click the button "Add Cloud" in the "cloud" add form
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "Bare Metal" provider should be added within 30 seconds

  @KVM-add
  Scenario: Add KVM
    When I click the fab button in the "dashboard" page
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "KVM (Via Libvirt)" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "KVM (Via Libvirt)" credentials
    And I focus on the button "Add Cloud" in the "cloud" add form
    Then I click the button "Add Cloud" in the "cloud" add form
    # w8 for it because KVM takes some time
    And I wait for 30 seconds
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "KVM" provider should be added within 30 seconds

  @machine-shell
  Scenario: Check shell access in other server
    When I visit the machines page after the counter has loaded
    And I wait for 10 seconds
    And I click the other server machine
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    When I click the "Shell" action button in the "machine" page
    Then I expect terminal to open within 3 seconds
    When I wait for 5 seconds
    And I type in the terminal "ls -l"
    And I wait for 2 seconds
    Then total should be included in the output
    And I close the terminal
