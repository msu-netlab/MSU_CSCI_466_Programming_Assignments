# CSCI 466 PA3 - Network Layer: Data Plane

## Instructions

Complete the following assignment in pairs, or groups of three. 
Submit your work on D2L into the "Programming Assignment&nbsp;3" folder before its due date. 
All partners will submit the same solution and we will only grade one solution for each group.


## Learning Objectives

In this programming assignment you will:

- Packetize streams at the network layer
- Implement packet segmentation
- Implement forwarding through routing tables


## Assignment

During this project, you will implement several key data plane functions of a router, including stream packetization, packet segmentation, and forwarding.
The next assignment will complement these functions at the control plane.


### Starting Code

The starting code for this project provides you with the implementation several network layers that cooperate to provide end-to-end communication.

```
NETWORK LAYER (network.py)
DATA LINK LAYER (link.py)
```

The code also includes `simulation.py` that manages the threads running the different network objects.
Currently, `simulation.py` defines the following network.

![Image of Yaktocat](https://octodex.github.com/images/yaktocat.png)

### Program Invocation

To run the starting code you may run:

```
python server.py 5000
```

and

```
python client.py localhost 5000
```

in separate terminal windows. 
Be sure to start the server first, to allow it to start listening on a socket, and start the client soon after, before the server times out.


## BONUS 

We will award __one bonus point__ for each of the following:

* The network layer may also reorder packets.
If you set `prob_pkt_reorder` to a non-zero probability you will start seeing packet that are reordered.
Implement RDT 3.1, which delivers packets in the correct order.

* RDT 3.1 is a stop and wait protocol.
Implements RDT 4.0 - a pipelined reliable data transmission protocol based on either Go-back-N (GBN), or Selective Repeat (SR) mechanisms.


## What to Submit

You will submit different versions of `rdt.py`, which implements the send and receive functions for RDT&nbsp;2.1, and RDT&nbsp;3.0.
RDT&nbsp;2.1 tolerates corrupted packets through retransmission.
RDT&nbsp;3.0 tolerates corrupted and lost packets through retransmission.
The necessary functions prototypes are already included in `rdt.py`.
For the purposes of testing you may modify `client.py` and `server.py` to use these functions instead of those of RDT&nbsp;1.0.
You will also submit a link to a YouTube video showing an execution of your code for each version of the protocol.
Videos longer than 5 minutes will not be graded.

## Grading Rubric

We will grade the assignment as follows:

* \[2 points\] `partners.txt` with your partner's first and last name.

* \[10 points\] `rdt_2_1.py`, `client_2_1.py`, `server_2_1.py`, `network_2_1.py` that correctly implement RDT&nbsp;2.1 and a link to a YouTube video showing the execution of your program.

  * \[2 points\] RDT&nbsp;2.1 delivers data under no corruption in the network

  * \[2 points\] RDT&nbsp;2.1 uses a modified Packet class to send ACKs

  * \[2 points\] RDT&nbsp;2.1 does not deliver corrupt packets

  * \[2 points\] RDT&nbsp;2.1 uses modified Packet class to send NAKs for corrupt packets

  * \[2 points\] RDT&nbsp;2.1 resends data following a NAK

* \[13 points\] `rdt_3_0.py`, `client_3_0.py`, `server_3_0.py`, `network_3_0.py` that correctly implement RDT&nbsp;3.0 and a link to a YouTube video showing the execution of your program.

  * \[2 points\] RDT&nbsp;3.0 delivers data under no corruption or loss in the network and uses a modified Packet class to send ACKs
  
  * \[2 points\] RDT&nbsp;3.0 does not deliver corrupt packets and uses modified Packet class to send NAKs
  
  * \[2 points\] RDT&nbsp;3.0 resends data following a NAK
  
  * \[2 points\] RDT&nbsp;3.0 retransmits a lost packet after a timeout
  
  * \[2 points\] RDT&nbsp;3.0 retransmits a packet after a lost ACK
  
  * \[3 points\] RDT&nbsp;3.0 ignores a duplicate packet after a premature timeout (or after a lost ACK)

* \[1 points\] (BONUS) `rdt_3_1.py`, `client_3_1.py`, `server_3_1.py`, `network_3_1.py` that correctly implement RDT&nbsp;3.1 and a link to a YouTube video showing the execution of your program.

* \[1 points\] (BONUS) `rdt_4_0.py`, `client_4_0.py`, `server_4_0.py`, `network_4_0.py` that correctly implement RDT&nbsp;4.0 and a link to a YouTube video showing the execution of your program.



## Acknowledgements

This project was adapted from Kishore Ramachandran version of this assignment.




