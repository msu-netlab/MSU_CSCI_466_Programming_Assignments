'''
Created on Oct 12, 2016

@author: mwitt_000
'''

import queue
import threading

## An abstraction of a link between router interfaces
class Link:
    
    ## creates a link between two objects by looking up and linking node interfaces.
    # @param from_node: node from which data will be transfered
    # @param from_intf_num: number of the interface on that node
    # @param to_node: node to which data will be transfered
    # @param to_intf_num: number of the interface on that node
    # @param mtu: link maximum transmission unit
    def __init__(self, from_node, from_intf_num, to_node, to_intf_num, mtu):
        self.from_node = from_node
        self.from_intf_num = from_intf_num
        self.to_node = to_node
        self.to_intf_num = to_intf_num
        self.in_intf = from_node.out_intf_L[from_intf_num]
        self.out_intf = to_node.in_intf_L[to_intf_num]
        #configure the linking interface MTUs
        self.in_intf.mtu = mtu
        self.out_intf.mtu = mtu
        
        
    ## called when printing the object
    def __str__(self):
        return 'Link %s-%d to %s-%d' % (self.from_node, self.from_intf_num, self.to_node, self.to_intf_num)
        
    ##transmit a packet from the 'from' to the 'to' interface
    def tx_pkt(self):
        pkt_S = self.in_intf.get()
        if pkt_S is None:
            return #return if no packet to transfer
        if len(pkt_S) > self.out_intf.mtu:
            print('%s: packet "%s" length greater then link mtu (%d)' % (self, pkt_S, self.out_intf.mtu))
            return #return without transmitting if packet too big
        #otherwise transmit the packet
        try:
            self.out_intf.put(pkt_S)
            print('%s: transmitting packet "%s"' % (self, pkt_S))
        except queue.Full:
            print('%s: packet lost' % (self))
            pass
        
        
## An abstraction of the link layer
class LinkLayer:
    
    def __init__(self):
        ## list of links in the network
        self.link_L = []
        self.stop = False #for thread termination
    
    ##add a Link to the network
    def add_link(self, link):
        self.link_L.append(link)
        
    ##transfer a packet across all links
    def transfer(self):
        for link in self.link_L:
            link.tx_pkt()
                
    ## thread target for the network to keep transmitting data across links
    def run(self):
        print (threading.currentThread().getName() + ': Starting')
        while True:
            #transfer one packet on all the links
            self.transfer()
            #terminate
            if self.stop:
                print (threading.currentThread().getName() + ': Ending')
                return
    