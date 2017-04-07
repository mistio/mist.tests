@clouds-add-b
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core

#  @cloud-add
#  Scenario Outline:
#    When I click the "new cloud" button with id "addBtn"
#    Then I expect the "Cloud" add form to be visible within max 5 seconds
#    When I select the "<provider>" provider
#    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
#    When I use my "<provider>" credentials
#    And I focus on the button "Add Cloud" in "cloud" add form
#    And I click the button "Add Cloud" in "cloud" add form
#    And I wait for the dashboard to load
#    And I scroll the clouds list into view
#    Then the "<provider>" provider should be added within 120 seconds
#
#
#    Examples: Providers
#    | provider       |
#    | Azure ARM      |
#    | Linode         |
#    | AWS            |
##    | Digital Ocean  | tested @ orchestration
##    | Vmware         |
##    | Indonesian     |
##    | KVM (Via Libvirt)           |
##    | Other Server   |
##    | HostVirtual    |

  @KVM-add
  Scenario: Add KVM
#    When I refresh the page
    When I add the key needed for KVM
    When I click the "new cloud" button with id "addBtn"
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "KVM (Via Libvirt)" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "KVM (Via Libvirt)" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    Then I click the button "Add Cloud" in "cloud" add form
    # w8 for it because KVM takes some time
    And I wait for 10 seconds
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "KVM" provider should be added within 20 seconds

  @bare-metal-add
  Scenario: Add bare-metal
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
  Scenario: Check shell access
    When I click the "docker-ui-test-machine-random" "machine"
    And I expect the "machine" edit form to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the button "Shell" from the menu of the "machine" edit form
    And I test the ssh connection
    And I wait for 1 seconds