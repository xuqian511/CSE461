# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 11:47:12 2020

@author: fghjk
"""
"""
 Build A Simple Network
H1 H2
 S1
H3 H4

Goal of part 1:
Modify file part1.py to create the following topology.
Some useful Mininet commands:
1. dump (dump info about all nodes)
2. pingall (Literally, ping all the connections)
3. ping (ping the connection h1 and h2)
4. iperf (Test the bandwidth between two hosts)
"""
#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.cli import CLI

class part1_topo(Topo):
    
    def build(self):
        pass
        #switch1 = self.addSwitch('switchname')
        #host1 = self.addHost('hostname')
        #self.addLink(hostname,switchname)
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)
        self.addLink(h4, s1)

topos = {'part1' : part1_topo}

if __name__ == '__main__':
    t = part1_topo()
    net = Mininet (topo=t)
    net.start()
    CLI(net)
    net.stop()

