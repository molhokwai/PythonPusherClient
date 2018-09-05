#!/usr/bin/env python

import sys
sys.path.append('..')

import time

import pusherclient
from plugin_pusher import settings

# Add a logging handler so we can see the raw communication data
import logging
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

global pusher

def print_usage(filename):
    print("Usage: python %s <appkey> <appcluster>" % filename)

def channel_callback(data):
    print("Channel Callback: %s" % data)

def connect_handler(data):
    for c in channel_names:
        if not channel_names[c][0]:
            channel = pusher.subscribe(c)

            _events = channel_names[c][1]
            for e in _events:
                if not _events[e]:
                    channel.bind(e, channel_callback)
                    _events[e] = True
            channel_names[c][0] = True


appkey = settings.appkey or None
appcluster = settings.appcluster or None
channel_names = settings.channel_names or {}

if __name__ == '__main__':    
    if not appkey:
        if len(sys.argv) != 3:
            print_usage(sys.argv[0])
            sys.exit(1)
        else:
            appkey = sys.argv[1]
            appcluster = sys.argv[2]

    """
        Changes:
        -------
            Cluster: Added cluster in host name (also in process file arguments)
            Channel names, event names: Added chosen event names binding for given channel name
            
            -   Added cluster<string> parameter (<Pusher>)
                >   Added cluster in host name in <Pusher.__init__>
                >   Removed <Pusher._build_url> @classmethod attribute
            -   Added event_names<list> parameter (<Pusher>, <Connection>)
                >   Added event_names binding in <Connection.__init__>
                
            @acknowledgement:   Pysher (https://github.com/nlsdfnbch/Pysher/blob/master/pysher/pusher.py)
            @framework:         Pusher (https://pusher.com/tutorials/chat-widget-python)
    """
    event_names = []
    for c in channel_names:
        event_names += channel_names[c][1].keys()
    pusher = pusherclient.Pusher(appkey, cluster=appcluster, event_names=event_names)
    pusher.connection.bind('pusher:connection_established', connect_handler)
        
    pusher.connect()
    print
    print '------------------------------------------------------------'
    print
    
    while True:
        time.sleep(1)
