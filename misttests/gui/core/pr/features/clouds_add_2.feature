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
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "<provider>" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    And I click the button "Add Cloud" in "cloud" add form
    And I wait for the links in homepage to appear
    And I scroll the clouds list into view
    Then the "<provider>" provider should be added within 120 seconds


    Examples: Providers
    | provider       |
    | Azure ARM      |
    | Linode         |
    | Softlayer      |
#    | Vmware         |
#    | Indonesian     |
#    | HostVirtual    |

#  @KVM-add
#  Scenario: Add KVM
#    When I refresh the page
#    When I add the key needed for Other Server
#    When I click the "new cloud" button with id "addBtn"
#    Then I expect the "Cloud" add form to be visible within max 5 seconds
#    When I select the "KVM (Via Libvirt)" provider
#    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
#    When I use my "KVM (Via Libvirt)" credentials
#    And I focus on the button "Add Cloud" in "cloud" add form
#    Then I click the button "Add Cloud" in "cloud" add form
#    # w8 for it because KVM takes some time
#    And I wait for 10 seconds
#    When I wait for the dashboard to load
#    And I scroll the clouds list into view
#    Then the "KVM" provider should be added within 20 seconds
#
  @bare-metal-add
  Scenario: Add bare-metal
    When I add the key needed for Other Server
    When I click the "new cloud" button with id "addBtn"
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "Other Server" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "Other Server" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    Then I click the button "Add Cloud" in "cloud" add form
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "Bare Metal" provider should be added within 20 seconds

  @machine-shell
  Scenario: Check shell access in bare metal
    When I visit the machines page
    And I wait for 2 seconds
    And I click the "Bare Metal" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Shell" from the menu of the "machine" edit form
    And I test the ssh connection
