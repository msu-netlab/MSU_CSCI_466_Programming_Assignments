import network
import link
import threading
from time import sleep
import sys

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 1   #give the network sufficient time to execute transfers

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads at the end
    
    #create network hosts
    host_1 = network.Host('H1')
    object_L.append(host_1)
    host_2 = network.Host('H2')
    object_L.append(host_2)
    
    #create routers and cost tables for reaching neighbors
    cost_D = {'H1': {0: 1}, 'RB': {1: 1}} # {neighbor: {interface: cost}}
    router_a = network.Router(name='RA', 
                              cost_D = cost_D,
                              max_queue_size=router_queue_size)
    object_L.append(router_a)

    cost_D = {'H2': {1: 3}, 'RA': {0: 1}} # {neighbor: {interface: cost}}
    router_b = network.Router(name='RB', 
                              cost_D = cost_D,
                              max_queue_size=router_queue_size)
    object_L.append(router_b)
    
    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links - need to reflect the connectivity in cost_D tables above
    link_layer.add_link(link.Link(host_1, 0, router_a, 0))
    link_layer.add_link(link.Link(router_a, 1, router_b, 0))
    link_layer.add_link(link.Link(router_b, 1, host_2, 0))
    
    
    #start all the objects
    thread_L = []
    for obj in object_L:
        thread_L.append(threading.Thread(name=obj.__str__(), target=obj.run)) 
    
    for t in thread_L:
        t.start()
    
    ## compute routing tables
    router_a.send_routes(1) #one update starts the routing process
    sleep(simulation_time)  #let the tables converge
    print("Converged routing tables")
    for obj in object_L:
        if str(type(obj)) == "<class 'network.Router'>":
            obj.print_routes()

    #send packet from host 1 to host 2
    host_1.udt_send('H2', 'MESSAGE_FROM_H1')
    sleep(simulation_time)
    
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")

