@clouds-add-b
Feature: Add second-tier clouds in Polymist

  Background:
    Given I am logged in to mist.core
    And I am in the new UI
    When I wait for the dashboard to load

  @cloud-add
  Scenario Outline:
    When I click the new cloud button
    Then I expect the "Cloud" add form to be visible within max 5 seconds
    When I select the "<provider>" provider
    Then I expect the field "Title" in the cloud add form to be visible within max 4 seconds
    When I use my "<provider>" credentials
    And I focus on the button "Add Cloud" in "cloud" add form
    Then I click the button "Add Cloud" in "cloud" add form
    When I wait for the dashboard to load
    And I scroll the clouds list into view
    Then the "<provider>" provider should be added within 120 seconds


    Examples: Providers
    | provider       |
#    | Docker         | -- tested @ cloud-actions
#    | Openstack      | -- tested @ cloud-actions
#    | Vultr          | -- tested @ rbac-rules
    | Azure ARM      |
    | Linode         |
    | AWS            |
    | Digital Ocean  |
#    | Vmware         |
#    | Indonesian     |
#    | KVM (Via Libvirt)           |
#    | Other Server   |
#    | HostVirtual    |
