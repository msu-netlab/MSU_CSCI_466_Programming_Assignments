import queue
import threading
from collections import defaultdict
import sys
import math


## wrapper class for a queue of packets
class Interface:
    ## @param maxsize - the maximum size of the queue storing packets
    def __init__(self, maxsize=0):
        self.in_queue = queue.Queue(maxsize)
        self.out_queue = queue.Queue(maxsize)

    ##get packet from the queue interface
    # @param in_or_out - use 'in' or 'out' interface
    def get(self, in_or_out):
        try:
            if in_or_out == 'in':
                pkt_S = self.in_queue.get(False)
                # if pkt_S is not None:
                #     print('getting packet from the IN queue')
                return pkt_S
            else:
                pkt_S = self.out_queue.get(False)
                # if pkt_S is not None:
                #     print('getting packet from the OUT queue')
                return pkt_S
        except queue.Empty:
            return None

    ##put the packet into the interface queue
    # @param pkt - Packet to be inserted into the queue
    # @param in_or_out - use 'in' or 'out' interface
    # @param block - if True, block until room in queue, if False may throw queue.Full exception
    def put(self, pkt, in_or_out, block=False):
        if in_or_out == 'out':
            # print('putting packet in the OUT queue')
            self.out_queue.put(pkt, block)
        else:
            # print('putting packet in the IN queue')
            self.in_queue.put(pkt, block)


## Implements a network layer packet.
class NetworkPacket:
    ## packet encoding lengths
    dst_S_length = 5
    prot_S_length = 1

    ##@param dst: address of the destination host
    # @param data_S: packet payload
    # @param prot_S: upper layer protocol for the packet (data, or control)
    def __init__(self, dst, prot_S, data_S):
        self.dst = dst
        self.data_S = data_S
        self.prot_S = prot_S

    ## called when printing the object
    def __str__(self):
        return self.to_byte_S()

    ## convert packet to a byte string for transmission over links
    def to_byte_S(self):
        byte_S = str(self.dst).zfill(self.dst_S_length)
        if self.prot_S == 'data':
            byte_S += '1'
        elif self.prot_S == 'control':
            byte_S += '2'
        else:
            raise ('%s: unknown prot_S option: %s' % (self, self.prot_S))
        byte_S += self.data_S
        return byte_S

    ## extract a packet object from a byte string
    # @param byte_S: byte string representation of the packet
    @classmethod
    def from_byte_S(self, byte_S):
        dst = byte_S[0: NetworkPacket.dst_S_length].strip('0')
        prot_S = byte_S[NetworkPacket.dst_S_length: NetworkPacket.dst_S_length + NetworkPacket.prot_S_length]
        if prot_S == '1':
            prot_S = 'data'
        elif prot_S == '2':
            prot_S = 'control'
        else:
            raise ('%s: unknown prot_S field: %s' % (self, prot_S))
        data_S = byte_S[NetworkPacket.dst_S_length + NetworkPacket.prot_S_length:]
        return self(dst, prot_S, data_S)


## Implements a network host for receiving and transmitting data
class Host:

    ##@param addr: address of this node represented as an integer
    def __init__(self, addr):
        self.addr = addr
        self.intf_L = [Interface()]
        self.stop = False  # for thread termination

    ## called when printing the object
    def __str__(self):
        return self.addr

    ## create a packet and enqueue for transmission
    # @param dst: destination address for the packet
    # @param data_S: data being transmitted to the network layer
    def udt_send(self, dst, data_S):
        p = NetworkPacket(dst, 'data', data_S)
        print('%s: sending packet "%s"' % (self, p))
        self.intf_L[0].put(p.to_byte_S(), 'out')  # send packets always enqueued successfully

    ## receive packet from the network layer
    def udt_receive(self):
        pkt_S = self.intf_L[0].get('in')
        if pkt_S is not None:
            print('%s: received packet "%s"' % (self, pkt_S))

    ## thread target for the host to keep receiving data
    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            # receive data arriving to the in interface
            self.udt_receive()
            # terminate
            if (self.stop):
                print(threading.currentThread().getName() + ': Ending')
                return


## Implements a multi-interface router
class Router:

    ##@param name: friendly router name for debugging
    # @param cost_D: cost table to neighbors {neighbor: {interface: cost}}
    # @param max_queue_size: max queue length (passed to Interface)
    def __init__(self, name, cost_D, max_queue_size):
        self.stop = False  # for thread termination
        self.name = name
        # create a list of interfaces
        self.intf_L = [Interface(max_queue_size) for _ in range(len(cost_D))]
        # save neighbors and interfeces on which we connect to them
        self.cost_D = cost_D  # cost_D {neighbor: {interface: cost}}
        # TODO: set up the routing table for connected hosts

        # {destination: {router: cost}} ##Initial setup
        self.rt_tbl_D = {name: {name: 0}}
        keys = list(cost_D.keys())
        values = list(cost_D.values())
        for i in range(len(keys)):
            self.rt_tbl_D[keys[i]] = {name: list(values[i].values())[0]}
        self.print_routes()
        print('%s: Initialized routing table' % self)

    def getCurrentRoutingTable(self):
        routingTableString = self.name + "-"
        values = list(self.rt_tbl_D.values())
        keys = list(self.rt_tbl_D.keys())
        first = True
        for i in range(len(keys)):
            if first:
                first = False
                routingTableString += keys[i] + "," + str(list(values[i])[0]) + "," + str(list(values[i].values())[0])
            else:
                routingTableString += ":" + keys[i] + "," + str(list(values[i])[0]) + "," + str(
                    list(values[i].values())[0])
        print(routingTableString)
        return routingTableString

    ## Print routing table
    def updateUniqueRouters(self):
        self.uniqueRouters = []
        values = self.rt_tbl_D.values()
        routers = {}
        for i in range(len(values)):
            if list(list(values)[i].keys())[0] not in routers:
                routers[list(list(values)[i].keys())[0]] = ""
        for item in routers:
            self.uniqueRouters.append(item)

    def print_routes(self):
        keys = self.rt_tbl_D.keys()
        values = self.rt_tbl_D.values()
        columns = len(keys) + 1
        keyString = ""
        topTableString = "╒"
        headerBottomTableString = "╞"
        tableRowSeperator = "├"
        tableBottom = "╘"
        # //Setting up table
        for i in range(columns):
            if (i + 1 != columns):
                topTableString += "══════╤"
                headerBottomTableString += "══════╪"
                tableRowSeperator += "──────┼"
                tableBottom += "══════╧"
            else:
                topTableString += "══════╕\n"
                headerBottomTableString += "══════╡\n"
                tableRowSeperator += "──────┤\n"
                tableBottom += "══════╛\n"
        itemSpace = "      "
        for item in keys:
            keyString += "  " + item + "  │"
        costRows = []
        changed = []
        self.updateUniqueRouters()
        for item in self.uniqueRouters:
            costRows.append("│  " + item + "  │")
        for i in range(len(values)):
            changedFlag = False
            for j in range(len(costRows)):
                for k in range(len(list(values)[i].keys())):
                    if list(list(values)[i].keys())[k] == self.uniqueRouters[j]:
                        formattedVal = itemSpace[0:len(itemSpace) - len(str(list(list(values)[i].values())[k]))] + str(
                            list(list(values)[i].values())[k])
                        costRows[j] += formattedVal + "│"
                        changed.append(j)
                        changedFlag = True
            if changedFlag:
                changedFlag = False
                for l in range(len(costRows)):
                    if (l in changed):
                        continue
                    else:
                        costRows[l] += "      │"
                changed = []

        sys.stdout.write(topTableString + "│  " + self.name + "  │" + keyString + "\n" + headerBottomTableString)
        for i in range(len(costRows)):
            if i + 1 != len(costRows):
                sys.stdout.write(costRows[i] + "\n" + tableRowSeperator)
            else:
                sys.stdout.write(costRows[i] + "\n")
        sys.stdout.write(tableBottom)

    ## called when printing the object
    def __str__(self):
        return self.name

    ## look through the content of incoming interfaces and
    # process data and control packets
    def process_queues(self):
        for i in range(len(self.intf_L)):
            pkt_S = None
            # get packet from interface i
            pkt_S = self.intf_L[i].get('in')
            # if packet exists make a forwarding decision
            if pkt_S is not None:
                p = NetworkPacket.from_byte_S(pkt_S)  # parse a packet out
                if p.prot_S == 'data':
                    self.forward_packet(p, i)
                elif p.prot_S == 'control':
                    self.update_routes(p, i)
                else:
                    raise Exception('%s: Unknown packet type in packet %s' % (self, p))

    ## forward the packet according to the routing table
    #  @param p Packet to forward
    #  @param i Incoming interface number for packet p
    def forward_packet(self, p, i):
        try:
            # TODO: Here you will need to implement a lookup into the
            # forwarding table to find the appropriate outgoing interface
            # for now we assume the outgoing interface is 1

            # we know the length of the shortest path
            # we know how many edges and verticies there are
            # we don't know what the shortest path is... like how is the program going to trace the path??
            # simple: we use the bellman ford equation as a verification instead of an algorithm

            # first, let's make it easy.
            dest = p.dst

            # then we'll set aside some variable for the node to forward to, let's call it v
            v_d = 999  # distance to v
            v = dest
            # cost_D {neighbor: {interface: cost}}
            # okay, so now we know where we're going.
            for header in self.rt_tbl_D:
                # for every node in the routing table,
                if header in self.cost_D:  # narrow it down to only neighbors
                    # header is in routing table and is reachable by the node
                    dest_d = int(self.rt_tbl_D[dest][self.name])  # distance to the destination
                    node_d = int(self.rt_tbl_D[header][self.name])  # distance to potential outgoing node
                    try:
                        if v_d > (node_d + dest_d):  # find the minimum
                            # new minimum
                            v_d = node_d
                            v = header
                    except KeyError:
                        print("Key Error: Neighbor is likely host")
            # new addition
            print(v)
            print(v_d)
            chosenVal = 999
            chosenRoute = ""
            if v not in self.cost_D:  # if v is NOT a neighbor
                for value in self.rt_tbl_D[v]:  # iterate through values
                    cost = self.rt_tbl_D[v][value]  # get cost in routing table
                    if int(cost) < int(chosenVal):  # find lowest cost router
                        chosenRoute = value
                        chosenVal = cost
                for key in self.cost_D[chosenRoute]:  # set the chosenRoutes interface
                    out_intf = key  # set the outgoing interface to the result.
            else:  # is a neighbor
                # @param cost_D: cost table to neighbors {neighbor: {interface: cost}}
                for key in self.cost_D[v]:  # iterate through values
                    out_intf = key  # set the outgoing interface to the result.
            try:
                self.intf_L[out_intf].put(p.to_byte_S(), 'out', True)  # send out
            except IndexError:
                print("Index out of range, %i" % out_intf)
            print('%s: forwarding packet "%s" from interface %d to %d' % \
                  (self, p, i, 1))
        except queue.Full:
            print('%s: packet "%s" lost on interface %d' % (self, p, i))
            pass

    ## send out route update
    # @param i Interface number on which to send out a routing update
    def send_routes(self, i):
        # TODO: Send out a routing table update
        # create a routing table update packet
        p = NetworkPacket(0, 'control', self.getCurrentRoutingTable())
        try:
            print('%s: sending routing update "%s" from interface %d' % (self, p, i))
            self.intf_L[i].put(p.to_byte_S(), 'out', True)
        except queue.Full:
            print('%s: packet "%s" lost on interface %d' % (self, p, i))
            pass

    ## forward the packet according to the routing table
    #  @param p Packet containing routing information
    def update_routes(self, p, i):
        # TODO: add logic to update the routing tables and
        # possibly send out routing updates
        updates = p.to_byte_S()[6:].split('-')
        name = updates[0]
        update = updates[1].split(":")
        updated = False
        # Raw updating
        for j in update:  # for each update
            items = j.split(",")  # items: 0=dest 1 1=dest 2 2=cost between dest 1 and dest 2
            if items[0] in self.rt_tbl_D:  # if dest 1 is in table headers
                values = list(self.rt_tbl_D.values())  # values is a list of dicts of form {router: cost}
                exists = False  # assume that it doesn't exist
                # already in table
                for i in range(len(values)):  # for as many values(which are mappings of dests to routers)
                    vks = list(values[i].keys())  # vks = list of routers in
                    for vk in vks:  # for each router in the router list,
                        if vk == items[1]:  # if the router is dest 2
                            self.rt_tbl_D[items[0]][items[1]] = items[2]  # set the cost of dest 1 to dest 2 in the table to the cost in items
                            # do stuff/compare
                            exists = True

                if not exists:  # will always default to this
                    self.rt_tbl_D[items[0]][items[1]] = items[2]  # set the cost of dest 1 to dest 2 in the table to the cost in items
                    updated = True
            else:
                self.rt_tbl_D[items[0]] = {items[1]: items[2]}
                updated = True

        '''for header in self.rt_tbl_D: #see if header is missing routers in its dict
            for router in self.uniqueRouters: #for each router,
                if router not in self.rt_tbl_D[header]: #if the router is NOT in the dict of the header
                    #put it in the header's dict, set cost to inf
                    self.rt_tbl_D[header][router] = 999 #basically infinity, right?
                    self.rt_tbl_D[router][header] = 999'''

        self.updateUniqueRouters()
        # run the algorithm on each router in the table
        router_count = len(self.uniqueRouters)
        print(router_count)
        for j in range(router_count):  # for every router (row) in the network,
            # step 1: set all unknowns to infinity
            for header in self.rt_tbl_D:
                # print("Detecting gaps for {} to {}".format(header,self.uniqueRouters[j]))
                if self.uniqueRouters[j] not in self.rt_tbl_D[header]:  # if the router is NOT in the dict of the header
                    # print("Gap filled {} to {}".format(header, self.uniqueRouters[j]))
                    # put it in the header's dict, set cost to inf
                    self.rt_tbl_D[header][self.uniqueRouters[j]] = 999  # basically infinity, right?
            # {header: {router: cost}}
            # bellman ford starts here
            # http://courses.csail.mit.edu/6.006/spring11/lectures/lec15.pdf
            # rt_tbl is a list of edges.
            self.updateUniqueRouters()
            # step 2: relax edges |V|-1 times
            for i in range(len(self.rt_tbl_D)):
                # for V-1 (the number of verticies minus one
                for u in self.rt_tbl_D:
                    # relax edge, represented as a call with the header
                    # for each vertex's neighbor,
                    for v in self.rt_tbl_D[u]:  # iterate through each outgoing edge
                        edge_distance = int(self.rt_tbl_D[u][v])
                        u_dist = int(self.rt_tbl_D[u][self.uniqueRouters[j]])  # distance to u vertex
                        v_dist = int(self.rt_tbl_D[v][self.uniqueRouters[j]])  # distance to v vertex
                        try:
                            if (u_dist > (v_dist + edge_distance)):
                                # if the edge plus the distance to vertex v is greater than the distance to u
                                self.rt_tbl_D[u][
                                    self.uniqueRouters[j]] = v_dist + edge_distance  # update the distance to u
                                updated = True
                                self.updateUniqueRouters()
                        except KeyError:
                            print("Key error exception occurred")
        if (updated):
            # cost_D {neighbor: {interface: cost}}
            for i in range(len(self.cost_D.values())):  # for all values
                for x in range(len(list(self.cost_D.values())[i].keys())):
                    interface = list(list(self.cost_D.values())[i].keys())[x]
                    self.send_routes(interface)
                    self.updateUniqueRouters()

    ## thread target for the host to keep forwarding data
    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            self.process_queues()
            if self.stop:
                print(threading.currentThread().getName() + ': Ending')
                return
