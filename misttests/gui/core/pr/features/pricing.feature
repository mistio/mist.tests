@pricing
Feature: Pricing

  @verify-attention-msg
  Scenario: Verify that notification about exceeding plan will be shown once machines are more than 5
    Given cloud "Docker" has been added via API request
    And cloud "GCE" has been added via API request
    When I am logged in to mist.core
    Then there should be a message with text "Attention: You have exceeded the limits of the Free plan! The Free plan includes unlimited clouds and up to 5 machines with monitoring for 1 of them. To continue using Mist.io upgrade your plan."

  @upgrade-plan-test
  Scenario: Verify that upgrade-plan functionality works as expected
    When I visit the Account page
    And I wait for 3 seconds
    And I click the "Billing" button with id "billing"
    And I wait for 1 seconds
    Then the current plan should be "FREE"
    When I click the upgrade button under small plan
    And I set the card details in the purchase plan dialog
    And I click the button "Purchase"
    And I wait for 12 seconds
    Then the current plan should be "SMALL"

  @verify-attention-msg-disappears
  Scenario: Verify that notification about exceeding plan does not exist after upgrading plan
    When I visit the Home page
    Then the attention message should be absent
