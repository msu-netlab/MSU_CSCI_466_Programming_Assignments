import queue
import threading

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
        for (node_a, node_a_intf, node_b, node_b_intf) in \
        [(self.node_1, self.node_1_intf, self.node_2, self.node_2_intf), 
         (self.node_2, self.node_2_intf, self.node_1, self.node_1_intf)]: 
            intf_a = node_a.intf_L[node_a_intf]
            intf_b = node_b.intf_L[node_b_intf]
            pkt_S = intf_a.get('out')
            if pkt_S is None:
                continue #continue if no packet to transfer
            #otherwise transmit the packet
            try:
                intf_b.put(pkt_S, 'in')
                print('%s: direction %s-%s -> %s-%s: transmitting packet "%s"' % \
                    (self, node_a, node_a_intf, node_b, node_b_intf, pkt_S))
            except queue.Full:
                print('%s: direction %s-%s -> %s-%s: packet lost' % \
                    (self, node_a, node_a_intf, node_b, node_b_intf))
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
    