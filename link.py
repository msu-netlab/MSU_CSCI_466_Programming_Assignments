'''
Created on Oct 12, 2016

@author: mwitt_000
'''

import queue
import threading
import time

## An abstraction of a link between router interfaces
class Link:
    
    ## creates a link between two objects by looking up and linking node interfaces.
    # @param node_1: node from which data will be transfered
    # @param node_1_intf: number of the interface on that node
    # @param node_2: node to which data will be transfered
    # @param node_2_intf: number of the interface on that node
    def __init__(self, node_1, node_1_intf, node_2, node_2_intf):
        self.node_1 = node_1
        self.node_1_intf = node_1_intf
        self.node_2 = node_2
        self.node_2_intf = node_2_intf
        print('Created link %s' % self.__str__())
        
    ## called when printing the object
    def __str__(self):
        return 'Link %s-%d - %s-%d' % (self.node_1, self.node_1_intf, self.node_2, self.node_2_intf)
        
    ##transmit a packet between interfaces in each direction
    def tx_pkt(self):
        for (node_a, node_a_intf, node_b, node_b_intf) in [(self.node_1, self.node_1_intf, self.node_2, self.node_2_intf), (self.node_2, self.node_2_intf, self.node_1, self.node_1_intf)]: 
            intf_a = node_a.intf_L[node_a_intf]
            intf_b = node_b.intf_L[node_b_intf]
            if intf_a.out_queue.empty():
                continue #continue if no packet to transfer
            #otherwise try transmitting the packet
            try:
                #check if the interface is free to transmit a packet
                if intf_a.next_avail_time <= time.time():
                    #transmit the packet
                    pkt_S = intf_a.get('out')
                    intf_b.put(pkt_S, 'in')
                    #update the next free time of the inteface according to serialization delay
                    pkt_size = len(pkt_S)*8 #assuming each characted is 8 bits
                    intf_a.next_avail_time = time.time() + pkt_size/intf_a.capacity                
                    print('%s: transmitting packet "%s" on %s %s -> %s, %s \n' \
                          ' - seconds until the next available time %f\n' \
                          ' - queue size %d\n' \
                          % (self, pkt_S, node_a, node_a_intf, node_b, node_b_intf, intf_a.next_avail_time - time.time(), intf_a.out_queue.qsize()))
                # uncomment the lines below to see waiting time until next transmission
#                 else:
#                     print('%s: waiting to transmit packet on %s %s -> %s, %s for another %f milliseconds' % (self, node_a, node_a_intf, node_b, node_b_intf, intf_a.next_avail_time - time.time()))    
            except queue.Full:
                print('%s: packet lost' % (self))
                pass
        
        
## An abstraction of the link layer
class LinkLayer:
    
    def __init__(self):
        ## list of links in the network
        self.link_L = []
        self.stop = False #for thread termination
        
    ## called when printing the object
    def __str__(self):
        return 'Network'
    
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
    