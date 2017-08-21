@ip-whitelisting
Feature: Ip-whitelisting


#-- New user can create resources (no whitelisted IPs)
#
#-- User saves his IP as whitelisted
#
#-- User can still create resources
#
#-- User updates whitelisted ips (removes his current IP, whitelisted IPs are now [])
#
#-- User can still create resources
#
#-- User saves a mock IP as whitelisted
#
#-- User gets 403 as responses (in everything except logout)
#
#-- User requests whitelist
#
#-- User confirms whitelist
#
#-- User can now successfully create resources
