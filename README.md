# CSCI 466 PA2 - Reliable Data Transmission (RDT)

## Instructions

Complete the following assignment in pairs, or groups of three. 
Submit your work on D2L into the "Programming Assignment&nbsp;2" folder before its due date. 
All partners will submit the same solution and we will only grade one solution for each group.


## Learning Objectives

In this programming assignment you will:

- Work with a layered network architecture
- Understand and implement the Stop-and-Wait Protocol with ACKs (Acknowledgments), NACKs (Negative
Acknowledgments), and re-transmissions


## Assignment

During this project, you will implement the Reliable Data Transmission protocols RDT 2.1, and RDT 3.0 discussed in class and the textbook, by extending an RDT 1.0 implementation.


### Starting Code

The starting code for this project provides you with the implementation of several network layers that cooperate to achieve end-to-end communication.

```
APPLICATION LAYER (client.py, server.py)
TRANSPORT LAYER (rdt.py)
NETWORK LAYER (network.py)
```

The client sends messages to the server, which converts them to pig latin and transmits them back.
The client and the server send messages to each other through the transport layer provided by an RDT implementation using the `rdt_1_0_send` and `rdt_1_0_receive` functions.
The starting `rdt.py` provides only the RDT 1.0 version of the protocol, which does not tolerate packet corruption, or loss.
The RDT protocol uses `udt_send` and `udt_receive` provided by `network.py` to transfer bytes between the client and server machines.
The network layer may corrupt packets or lose packets altogether.
`rdt.py` relies on the `Packet` class (in the same file) to form transport layer packets.

Your job will be to extend `rdt.py` to tolerate packet corruption and loss.
The provided code  lists prototype send and receive functions for these protocols.
You may need to modify/extend the `Packet` class to transmit the necessary information for these functions to work correctly.
The provided implementation of `network.py` is reliable, but we will test your code with non-zero probability for packet corruption and loss by changing the values of `prob_pkt_loss` and `prob_byte_corr` of the `NetworkLayer` class.
You should change those variables yourself to test your code and show that your protocol implementations tolerate corruption and loss in your demonstration videos.

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




