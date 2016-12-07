# Created by spiros at 7/12/2016
Feature: Machine actions for polymer

  Background:
    Given I am logged in to mist.core
    And I am in the new UI


  @machine-create
  Scenario: Create a machine
    When I wait for the dashboard to load
    Given "EC2" cloud has been added
    