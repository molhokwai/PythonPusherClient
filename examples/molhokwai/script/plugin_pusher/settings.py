#!/usr/bin/env python

appkey = '1ed4f14aec1b394a4ed4'
appcluster = 'eu'
# channel_names { [name] : [ subscribed (bool), event_names { [name] : bound (bool) } ] }
channel_names = { 'general-channel': [False, { 'client-guest-new-message': False }] }
