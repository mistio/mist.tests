@ip-whitelisting
Feature: Ip-whitelisting

  @whitelist-current-ip
  Scenario:  User whitelists his current IP
    Given I am logged in to mist.core
    When I visit the Account page
    And I wait for 3 seconds
    Then I click the "Whitelisted IPs" button with id "ips"


#-- User can still create resources
#
#-- User updates whitelisted ips (removes his current IP, whitelisted IPs are now [])
#
#-- User can still create resources



##############################################################
#-- User saves a mock IP as whitelisted
#
#-- User gets 403 as responses (in everything except logout)
#
#-- User requests whitelist
#
#-- User confirms whitelist
#
#-- User can now successfully create resources
