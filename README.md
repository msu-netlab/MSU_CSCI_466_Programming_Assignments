# CSCI 466 Programming Assignment - MPLS 

## Instructions
### Due: 12/12/17 11:59PM


Complete the following assignment in pairs, or groups of three. 
Submit your work into the Dropbox on D2L into the “Programming Assignment 5” folder. 
All partners will submit the same solution and we will only grade one solution for each group.


## Learning Objectives

In this lab you will:

- Implement MPLS forwarding on routers
- Control forwarding paths using MPLS labels
- Implement priority-based forwarding on routers


## Overview

In this project, you will implement MPLS forwarding and priority-based forwarding at routers.
In this assignment you will also have a greater autonomy over and responsibility for the design of your protocol based on the requirements. 

### Starting Code 

The code provides you with the implementation several network layers that cooperate to provide end-to-end communication. 

```
NETWORK LAYER (network.py) 
DATA LINK LAYER (link.py) 
```

The code also includes `simulation.py` that manages the threads running the different network objects. Currently, `simulation.py` defines the following network.

<!-- ![image](images/simple.png) -->
<img src="images/simple.png" alt="Drawing" style="width:400pt; height:100pt"/>

At a high level a network defined in `simulation.py` includes hosts, routers and links. 
`Hosts` generate and receive traffic. 
`Routers` encapsulate packets as MPLS frames, forward them based on MPLS tables, and decapsulate them on the last hop to deliver network traffic to hosts.
`Links` connect network interfaces of routers and hosts. 
Finally, the `LinkLayer` forwards traffic along links.
In this assignment forwarding speed is restricted by link capacity. 
Please consult the [video lecture](https://www.youtube.com/watch?v=vsB5zJLCU2k) for a more in-depth explanation of the code.

### Program Invocation

To run the starting code you may execute:

```
python simulation.py
```

The current `simulation_time` in `simulation.py` is __10 second__ to account for the delay of packet forwarding. 
As the network becomes more complex and takes longer to execute, you may need to extend the simulation to allow all the packets to be transfered.



## Assignment

1. [X points] Implement MPLS forwarding

	a. [X points] Implement MPLS frame class to encapsulate NetworkPackets. 
	When a NetworkPacket arrives from a host at a router, the router should encapsulate the packet in an MPLS frame. 
	In the slides we presented the MPLS frame structure and position with respect to link (Ethernet) and
network (IP) layer packets as:

	<!-- ![image](images/simple.png) -->
	<img src="images/simple.png" alt="Drawing" style="width:400pt; height:100pt"/>

	In the context of this project, where we have no link-layer frame and we do have a NetworkPacket,
your transmissions should look like:

	<!-- ![image](images/simple.png) -->
	<img src="images/simple.png" alt="Drawing" style="width:400pt; height:100pt"/>

	The MPLS frame should contain the label at the least. 
	You may add experimental bits, S bit, and time to live if you choose. 

	b. [X points] Modify `Router()` constructor to accept MPLS forwarding tables. 
	The tables should contain the in label, in intf, out label, and out intf. 
	Pass in correctly designed forwarding tables so that your routers achieve end-to-end connectivity and forward traffic from different hosts on different paths.

	c. [X points] Modify Router.forward packet() function to encapsulate and decapsulate packets and
to forward MPLS frames. 
	Only links incident on hosts should carry NetworkPackets. 
	Other links should only carry MPLS frames.


Submit a YouTube video link showing the execution of `simulation.py` until routing tables converge.
	We will grade you based on the formatting routing tables, the content of your route update messages, and the final state of your routing tables.
	Make sure that all of these are clearly visible in your output.
	Submit your code as `link_1.py`, `network_1.py`, and `simulation_1.py`.



2. [X points] Your next task is to implement MPLS forwarding, such that packets from different hosts follow different paths. 
In this part use the following topology, with both Host 1 and Host 2 sending packets to Host 3.
As before, you should control the forwading between routers using MPLS tables passed to `Router` constructors.

	<img src="images/complex.png" alt="Drawing" style="width:400pt; height:100pt"/>
	<!-- ![image](images/complex.png)  -->

Submit a YouTube video link showing the execution of `simulation.py` until routing tables converge.
	We will grade you based on the formatting routing tables, the content of your route update messages, and the final state of your routing tables.
	Make sure that all of these are clearly visible in your output.
	Submit your code as `link_1.py`, `network_1.py`, and `simulation_1.py`.

3. [X points]

	Implement priority forwarding on your MPLS routers. Remember that priority is origi- nally carried in the NetworkPacket. You will need to devise a method for your routers to somehow have access to packet priority (there are three good alternative solutions for implementing this).

	When running the code you will notice a bottleneck exists on the outgoing interface 0 of
Router B. The output shows you the remaining queue size after a packet is transmitted over a link. Your
first task is to implement strict priority forwarding to make sure that higher priority packets skip over
lower priority packets in the outgoing queue.

	a. [3 points] The udt send() function in simulation.py sends packet with priorities 0 and 1. Assume higher number priorities are higher priorities, i.e. 1 is higher than 0. Extend the NetworkPacket to carry the priority number with which it was sent.
	
	b. [3 points] At each router implement strict priority forwarding. My suggestion would be to change the implementation of Interface.get(), but other approaches are possible as well.
	
	c. [3 points] Modify the output to show that packets with priority 1 are forwarded first if the interface outgoing queue has packets of mixed priorities. Specifically the current output shows the queue size of an outgoing interface as: 

	```
	Link Host_1-0 - Router_A-0: transmitting packet ...
	- seconds until the next available time 0.416000
	- queue size 3
	```
	Modify that output to show the number of packets queued at each priority level as:
	
	```
	Link Host_1-0 - Router_A-0: transmitting packet ...
	- seconds until the next available time 0.416000
	- queue size 3: priority 0: X packets, priority 1: Y packets
	```

	d. [1 point] Make sure that output at the host shows what priority packet has been received. Hint: you should be able to get this ‘for free’ by correctly modifying NetworkPacket to carry the priority. 
	

Submit a YouTube video link showing the execution of `simulation.py` until routing tables converge.
	We will grade you based on the formatting routing tables, the content of your route update messages, and the final state of your routing tables.
	Make sure that all of these are clearly visible in your output.
	Submit your code as `link_1.py`, `network_1.py`, and `simulation_1.py`.


4. [1 point] BONUS: Implement Weighted fair queuing (WFQ) instead of strict priority in question 3.

Submit `link_4.py`, `network_4.py`, and `simulation_4.py`.


5. [1 point] BONUS: Implement a central controller to automatically configure MPLS forwarding tables in question 2 based on a global knowledge of network topology. 

Submit `link_5.py`, `network_5.py`, and `simulation_5.py`.



