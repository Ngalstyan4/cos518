#!/usr/bin/python

import sys

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import lg
from mininet.node import Node
from mininet.topolib import TreeTopo
from mininet.topo import Topo
from mininet.util import waitListening

# needed for network rate limiting
from mininet.util import dumpNodeConnections
from mininet.node import CPULimitedHost
from mininet.link import TCLink
SERVER_PROGRAM= '/home/ubuntu/anaconda3/bin/python flask_app.py'
def TreeNet( depth=1, fanout=2, **kwargs ):
    "Convenience function for creating tree networks."
    "Connects the root switch to all of child nodes directly"
    topo = TreeTopo( depth, fanout )
    return Mininet( topo, **kwargs )

class SingleSwitchTopo( Topo ):
    "Single switch connected to n hosts."
    def build( self, delays ):
        switch = self.addSwitch( 's1' )
        n = 4
        for i,delayInfo in enumerate(delays):
            # Each host gets 50%/n of system CPU
            print (delayInfo)
            host = self.addHost( delayInfo['name'])
            #,cpu=.5/n )
            # 10 Mbps, 5ms delay, 2% loss, 1000 packet queue
            ## link characteristics:

            # the first one is the cache @ address 10.0.0.1
            self.addLink( host, switch, delayInfo['bw'], delay=delayInfo['delay'],
                          max_queue_size=1000 )
        #linkopts = dict(bw=15, delay='2ms', loss=0, use_htb=True)
        #self.addLink(h, switch, **linkopts)

def SingleSwitchNet(delays, **kwargs):
    topo = SingleSwitchTopo(delays)
    return Mininet(topo, host=CPULimitedHost, link=TCLink, **kwargs)

def connectToRootNS( network, switch, ip, routes ):
    """Connect hosts to root namespace via switch. Starts network.
      network: Mininet() network object
      switch: switch to connect to root namespace
      ip: IP address for root namespace node
      routes: host networks to route to"""
    # Create a node in root namespace and link to switch 0
    root = Node( 'root', inNamespace=False )
    intf = network.addLink( root, switch ).intf1
    root.setIP( ip, intf=intf )
    # Start network that now includes link to root namespace
    network.start()
    # Add routes from root ns to hosts
    for route in routes:
        root.cmd( 'route add -net ' + route + ' dev ' + str( intf ) )

def cache( network, cmd=SERVER_PROGRAM, opts='',
          ip='10.123.123.1/32', routes=None, switch=None ):
    """Start a network, connect it to root ns, and run sshd on all hosts.
       ip: root-eth0 IP address in root namespace (10.123.123.1/32)
       routes: Mininet host networks to route to (10.0/24)
       switch: Mininet switch to connect to root namespace (s1)"""
    if not switch:
        switch = network[ 's1' ]  # switch to use
    if not routes:
        routes = [ '10.0.0.0/24' ]
    connectToRootNS( network, switch, ip, routes )
    for host in network.hosts:
        host.cmd( cmd + ' ' + opts + '&' )
    print "*** Waiting for daemons to start"
    #for server in network.hosts:
    #   waitListening( server=server, port=8000, timeout=5 )

    print
    print "*** Hosts are running sshd at the following addresses:"
    print
    for host in network.hosts:
        #host.cmd( 'kill %' + cmd )
        print host.name, host.IP()
    print
    print "*** Type 'exit' or control-D to shut down network"
    CLI( network )
    for host in network.hosts:
        host.cmd( 'kill %' + cmd )
    network.stop()

if __name__ == '__main__':
    lg.setLogLevel( 'info')
    UNIFORM_DELAY = '1ms'
    MED_DELAY = '1ms'
    HIGH_DELAY = '200ms'
    delays = [{'name':'cache', 'bw':10, 'delay':0},
              {'name':'db1', 'bw':10, 'delay':HIGH_DELAY},
              {'name':'db2', 'bw':10, 'delay':MED_DELAY},
              {'name':'db3', 'bw':10, 'delay':UNIFORM_DELAY},
              {'name':'db4', 'bw':10, 'delay':UNIFORM_DELAY},
              {'name':'db5', 'bw':10, 'delay':UNIFORM_DELAY},
              {'name':'db6', 'bw':10, 'delay':UNIFORM_DELAY},
    ]
    net = SingleSwitchNet(delays)
    # get sshd args from the command line or use default args
    # useDNS=no -u0 to avoid reverse DNS lookup timeout
    cache( net)
