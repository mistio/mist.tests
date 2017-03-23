@clouds
Feature: Add second-tier clouds

  Scenario:
    Given I am logged in to mist.core
    Given "EC2" cloud has been added
    Given "Azure" cloud has been added
    Given "Linode" cloud has been added
    Then I wait for 200 seconds
    Then I logout
