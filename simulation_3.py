import network_3
import link_3
import threading
from time import sleep
import sys

# configuration parameters
router_queue_size = 0  # 0 means unlimited
simulation_time = 10  # give the network_3 sufficient time to execute transfers
if __name__ == '__main__':
    object_L = []  # keeps track of objects, so we can kill their threads at the end
    # create network_3 hosts
    host_1 = network_3.Host('H1')
    host_2 = network_3.Host('H2')
    # {neighbor: {interface: cost}}
    cost_d_a = {'H1': {0: 5}, 'RB': {1: 4}, 'RC': {2: 1}}
    cost_d_b = {'RA': {0: 3}, 'RD': {1: 1}}
    cost_d_c = {'RA': {0: 1}, 'RD': {1: 3}}
    cost_d_d = {'RB': {0: 1}, 'RC': {1: 1}, 'H2': {2: 5}}
    router_a = network_3.Router('RA', cost_d_a, router_queue_size)
    router_b = network_3.Router('RB', cost_d_b, router_queue_size)
    router_c = network_3.Router('RC', cost_d_c, router_queue_size)
    router_d = network_3.Router('RD', cost_d_d, router_queue_size)
    object_L.append(host_1)
    object_L.append(host_2)
    object_L.append(router_a)
    object_L.append(router_b)
    object_L.append(router_c)
    object_L.append(router_d)
    # create a link_3 Layer to keep track of link_3s between network_3 nodes
    link_layer = link_3.LinkLayer()
    object_L.append(link_layer)

    # add all the links - need to reflect the connectivity in cost_D tables above
    link_layer.add_link(link_3.Link(host_1, 0, router_a, 0))
    link_layer.add_link(link_3.Link(router_a, 1, router_b, 0))
    link_layer.add_link(link_3.Link(router_a, 2, router_c, 0))
    link_layer.add_link(link_3.Link(router_c, 1, router_d, 1))
    link_layer.add_link(link_3.Link(router_b, 1, router_d, 0))
    link_layer.add_link(link_3.Link(router_d, 2, host_2, 0))


    # start all the objects
    thread_L = []
    for obj in object_L:
        thread_L.append(threading.Thread(name=obj.__str__(), target=obj.run))
    sys.stdout.write("\n")
    for t in thread_L:
        t.start()

    # compute routing tables
    router_d.send_routes(1)  # one update starts the routing process
    router_a.send_routes(1)
    sleep(simulation_time)  # let the tables converge
    print("Converged routing tables")
    # Table Header Bottom
    for i in range(len(object_L)):
        if str(type(object_L[i])) == "<class 'network_3.Router'>":
            object_L[i].print_routes()

    # send packet from host 1 to host 2
    host_1.udt_send('H2', 'MESSAGE_FROM_H1')
    host_2.udt_send('H1', 'MESSAGE FROM H2')
    sleep(simulation_time)

    # join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()

    print("All simulation threads joined")
