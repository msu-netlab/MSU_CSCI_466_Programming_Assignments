# CSCI 466 PA1 - Rock Paper Scissors Client-Server Application 

## Instructions
### Due: 9/11/2020 11:59PM

Complete the following assignment by yourself, or in a group of two.
Submit your work on D2L into the "Programming Assignment 1" folder. 


## Learning Objectives

In this programming assignment you will:

- Write an HTTP client-server application
- Design a messaging standard


## Overview

In this programming assignment you will implement a client-server version of the [rock paper scissors](https://en.wikipedia.org/wiki/Rock_paper_scissors) game.
<p align="center">
<img src="https://inteng-storage.s3.amazonaws.com/images/uploads/sizes/RPS_resize_md.jpg" alt="Rock Paper Scissors game" width="300">
</p>
Two players will throw rock, paper, or scissors by sending messages to the server.
The server will decide which player wins a particular *play*.
The players will then be able to query the server for the result of a play, as well as the overall score of a series of plays that comprise a *game*, for example best two plays out of three.



## Requirements

You will implement a client-server implementation of the rock paper scissors game.
Client and server programs will be implemented in Python and communicate via HTTP messages only.
Client and server programs may run on separate machines, for example on AWS EC2 instances, but may also run on the same machine with their sockets bound to different ports.

You will store your code in a __private__ [GitHub](https://github.com/) repository to prevent other teams from copying your code.

*Note: You may get access to AWS EC2 instances through [AWS Educate](https://aws.amazon.com/education/awseducate/). 
Make sure though to not publish your instance keys to your repository - if the repository is not private, your keys will be stolen and used to mine cryptocurrency depleting your AWS credits.*

### Client

The client will run on the command line and expose a text interface that lets users trigger its actions.
The client will send appropriate [`HTTP` requests](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol#Request_methods) to the server and process `HTTP` replies.
Client actions should include:
    
- Making a play by sending a message to the server.
  The message should indicate the type of a play (rock, paper, or scissors) and a unique identification of the play, to differentiate it from other plays that make up a game.
  I suggest that you assign each play to a resource ([URL](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)).
  You may also pass information through a [query string](https://en.wikipedia.org/wiki/Query_string).
- Checking the result of a play and displaying it to the user.
- Checking the score of a game (the number of won and lost plays) and displaying it to the user.
  I suggest that you also treat a game as a resource and I leave it to you to design how to do that.
- Resetting a game. 
    
### Server

The server will run on the command line and may produce diagnostic output, which however will not be accessible to users.
The server will accept `HTTP` messages from the client and respond with appropriate [`HTTP` status codes.](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#:~:text=final%20HTTP%20message.-,2xx%20Success,received%2C%20understood%2C%20and%20accepted.&text=Standard%20response%20for%20successful%20HTTP,on%20the%20request%20method%20used.)
Server actions should include:
    
- Accepting a play message. 
A player should not be able to make two different throws for the same play.
- Accepting a query for a play result and replying with the result for the specified play.
- Accepting a query for game score and replying with the score for the specified game.
- Accepting a game reset message and deleting plays that make up the game. 
A game should be reset only if both players request a reset.
Recall that HTTP servers do not keep any information in memory between requests, so you will need to use another method to keep track of the number of reset requests and who sent them.


### Program Invocation

Your server process should accept a port parameter, on which a clients can connect. 
For example, `python server.py 5000`.

Your client process should accept the IP address and the port of the server process.
For example, `python client.py 128.111.52.245 5000`.


## BONUS

I will award __one bonus point__ for the group that implements the most visually appealing user experience. 
To do so you may depart from the text interface requirement and use Python GUI packages, or implement the client in a browser using JavaScript.


## What to Submit

* \[1 point\] Submit a `partner.txt` file.
If you're working with a partner, `partner.txt` should include the name of your partner.
If you're working by yourself, `partner.txt` should include the word "solo".

* \[1 point\] Submit a `contributors.png` file.
The file should be a screenshot of the `contributors` page for your github repo, for example [https://github.com/msu-netlab/MSU_CSCI_466_Programming_Assignments/graphs/contributors] for the programming assignment repository. 
I will consult this screenshot and adjust partner grades in case there are discrepancies in effort.

* \[18 points\] Submit a zip archive of your code and a link to a YouTube video showing the execution of your program.
Make sure your videos are under 5 minutes long - __we will only watch the first five minutes of your video__.
We will award points for your implementation as follows, so make sure your video shows the appropriate functionality.
    
    * \[2 points\] Client sends an appropriate `HTTP` message to issue a play throw and processes an appropriate `HTTP` status code in the reply. 
    * \[2 points\] Client sends an appropriate `HTTP` message to check play result and displays the result to the user based on information in the `HTTP` reply.
    * \[1 point\] Server correctly computes results based on submitted throws.
    * \[3 point\] Server does not accept duplicate throws by players for the same play. Duplicate throws are rejected by the server via an appropriate `HTTP` status code in the reply. Based on the server reply the client notifies the user that the issued throw was a duplicate.
    * \[2 point\] Client sends an appropriate `HTTP` message to check play result and displays the result to user based on information included in the `HTTP` reply from the server.
    * \[2 point\] Client sends an appropriate `HTTP` message to check game score and displays the score to user based on information included in the `HTTP` reply from the server.
    * \[1 point\]  Client and server communicate only via `HTTP` messages. 
    * \[1 point\] Server does not keep any in-memory state, but uses on-disk resources to maintain rock paper scissors game state.
    * \[2 point\]  Client sends an appropriate `HTTP` message to reset a game. The server resets the game only if both clients request a reset.
    * \[1 point\]  Server notifies clients that a game has been reset using an appropriate `HTTP` reply.
    * \[1 point\]  Server does not use memory to keep track of reset requests.
    
    

