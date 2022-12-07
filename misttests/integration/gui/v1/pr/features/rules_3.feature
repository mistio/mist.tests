@rules-3
Feature: Rules

  @log-rule-on-org-webhook
  Scenario: Add rule from rules section that applies on organization. If triggered, send a webhook to slack
    Given I am logged in to mist
    And cloud "Docker" has been added via API request
    And I have given card details if needed
    And key "Key1" has been added via API request
    When I visit the Rules page
    And I click the button "add new rule" in the "rules" page
    And I wait for 1 seconds
    And I select the "organization" apply-on when adding new rule in the "rules" page
    And I type "type:request AND action:add_key" in the target when adding new rule in the "rules" page
    And I select the ">" operator when adding new rule in the "rules" page
    And I type "0" in the threshold when adding new rule in the "rules" page
    And I select the "webhook" action when adding new rule in the "rules" page
    And I type "SLACK_WEBHOOK_URL" in the webhook-url when adding new rule in the "rules" page
    And I type "{"Content-type" : "application/json"}" in the http-headers when adding new rule in the "rules" page
    And I type "{"text": "Incident triggered. Someone created a key!"}" in the json-body when adding new rule in the "rules" page
    And I save the new rule in the "rules" page
    And I wait for 10 seconds
    When I visit the Keys page
    When I click the button "+"
    Then I expect the "Key" add form to be visible within max 10 seconds
    When I set the value "TestKey" to field "Name" in the "key" add form
    And I focus on the button "Generate" in the "key" add form
    And I click the button "Generate" in the "key" add form
    Then I expect for the button "Add" in the "key" add form to be clickable within 22 seconds
    When I focus on the button "Add" in the "key" add form
    And I click the button "Add" in the "key" add form
    Then I expect the "key" page to be visible within max 10 seconds
    When I visit the Keys page
    Then "TestKey" key should be present within 15 seconds
    And a new webhook alert should have been posted in slack channel "SLACK_WEBHOOK_CHANNEL" within 90 seconds

  @log-rule-rules-page-alert
  Scenario: Insert rule regarding log from rules page. If triggered, alert
    When I visit the Rules page
    And I click the button "add new rule" in the "rules" page
    And I wait for 1 seconds
    And I select the "cloud" apply-on when adding new rule in the "rules" page
    And I select the "all" resource-type when adding new rule in the "rules" page
    And I select the "log" target-type when adding new rule in the "rules" page
    And I type "type:request AND action:create_machine" in the target when adding new rule in the "rules" page
    And I select the ">" operator when adding new rule in the "rules" page
    And I type "0" in the threshold when adding new rule in the "rules" page
    And I select the "alert" action when adding new rule in the "rules" page
    And I select the "info" alert-level when adding new rule in the "rules" page
    And I select the "Owners" team when adding new rule in the "rules" page
    And I wait for 1 seconds
    And I save the new rule in the "rules" page
    And I wait for 30 seconds

  @incident-triggered
  Scenario: Verify that incident gets triggered
    Given Docker machine "rules-test-machine-1-random" has been added via API request
    When I visit the Home page
    And I wait for the navigation menu to appear
    And I open the cloud page for "Docker"
    And I wait for 1 seconds
    Then I should see a(n) "request" log entry of action "create_machine" added "a few seconds ago" in the "cloud" page within 20 seconds
    When I visit the Machines page
    And I clear the search bar
    And I wait for 1 seconds
    And I search for "rules-test-machine-1-random"
    Then "rules-test-machine-1-random" machine should be present within 60 seconds
    And I should receive an email at the address "EMAIL" with subject "*** INFO *** cloud `Docker`: count of matching logs" within 180 seconds

  @log-rule-machine-page-alert
  Scenario: Insert rule regarding log from machine page. If triggered, alert
    When I click the "rules-test-machine-1-random" "machine"
    And I wait for 2 seconds
    And I scroll to the rules section in the "machine" page
    And I wait for 1 seconds
    And I click the button "add new rule" in the "machine" page
    And I wait for 1 seconds
    And I select the "log" target-type when adding new rule in the "machine" page
    And I type "type:request AND action:stop_machine" in the target when adding new rule in the "machine" page
    And I select the "=" operator when adding new rule in the "machine" page
    And I type "1" in the threshold when adding new rule in the "machine" page
    And I select the "alert" action when adding new rule in the "machine" page
    And I select the "info" alert-level when adding new rule in the "machine" page
    And I select the "Owners" team when adding new rule in the "machine" page
    And I wait for 2 seconds
    And I save the new rule in the "machine" page
    And I wait for 30 seconds

  @incident-triggered
  Scenario: Verify that incident gets triggered
    When I scroll to the top of the page
    And I click the "Stop" action button in the "machine" page
    Then I expect the "Stop Machine" dialog to be open within 4 seconds
    When I click the "Stop" button in the "Stop Machine" dialog
    Then I should receive an email at the address "EMAIL" with subject "*** INFO *** machine `rules-test-machine-1-random`: count of matching logs" within 180 seconds
