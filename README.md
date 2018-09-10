# CSCI 466 PA1 - Battleship Network Application 

## Instructions
### Due: 9/24/17 11:59PM


Complete the following assignment in pairs, or groups of three. 
Submit your work on D2L into the "Programming Assignment 1" folder. 
All partners will submit the same solution and we will only grade one solution for each group.


## Learning Objectives

In this programming assignment you will:

- Write a client-server application
- Communicate using HTTP
- Design a messaging standard


## Overview

In this lab you will write a distributed implementation of the 
[Battleship](https://en.wikipedia.org/wiki/Battleship_\(game\)) game.
We will use the standard [10x10 variation of the game](https://en.wikipedia.org/wiki/Battleship_\(game\)#Description).
Here is an [online implementation](http://www.battleshiponline.org/) of the Battleship game.
*Note that the ships in that implementation have slightly different names.*

Our implementation will be based on a symmetric client server architecture, where each player has both a server and a client.
The server keeps an internal state of the game and issues replies to the other player's client.



## Board Setup

The first step before the game begins is the setup of the board, according to the [rules of the game](https://en.wikipedia.org/wiki/Battleship_\(game\)#Description).
We will represent the board with a character array, where `_` represents water and Carrier, Battleship, cRuiser, Submarine, and Destroyer fields are represented by `C`, `B`, `R`, `S`, `D` respectively. 
For example, your board might be set up as follows:

```
CCCCC_____
BBBB______
RRR_______
SSS_______
D_________
D_________
__________
__________
__________
__________
```

You will save your board as `own_board.txt`.

### Messages

To play the game, your implementation needs to exchange two types of messages - `fire` and `result`.
The `fire` message needs to communicate the grid location of salvo.
The `result` message needs to communicate whether the salvo was a hit, a sink, or a miss.

The `fire` message will be represented as an `HTTP POST`.
The content of the fire message will include the targeted coordinates as a [URL formatted string for Web forms](\href{https://en.wikipedia.org/wiki/Query_string#Web_forms), for example 5 and 7, as: `x=5&y=7`.
Assume that coordinates are 0-indexed.
So, assuming that your opponent's server runs at `111.222.333.444:5555`, the `fire` message is a `POST` request sent to `http://111.222.333.444:5555?x=5&y=7`.

The `result` message will be formatted as an HTTP response.
For a correctly formatted `fire` request your reply will be an `HTTP OK` message with `hit=` followed by `1` (hit), or `0` (miss).
If the hit results in a sink, then the response will also include `sink=` followed by a letter code (`C`, `B`, `R`, `S`, `D`) of the sunk ship.
An example of such a reply is `hit=1\&sink=D`.

If the fire message includes coordinates that are out of bounds, the response will be `HTTP Not Found`.
If the fire message includes coordinates that have been already fired opon, the response will be `HTTP Gone`.
Finally, if the fire message is not formatted correctly, the response will be `HTTP Bad Request`.
For your reference here's a [link](\href{https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) to the different HTTP response status codes.


### Program Invocation

Your server process should accept a port parameter, on which a client can connect, and the file containing the setup of your board, eg. 

`python server.py 5000 own_board.txt`.

Your client process should accept the IP address, the port of the server process, and the X and Y coordinates onto which to fire, eg. 

`python client.py 128.111.52.245 5000 5 7`.

The client will be invoked multiple times during the game. 


### Internal State Representation
Following each `fire` message the server should update the state of the player's `own_board.txt` (whether a player's ship has been hit and where).
Following each `result` message the client should update the record of the player's shots onto the opponent's board, represented internally as `opponent_board.txt`.
A player should be able able to visually inspect their own board and their record of opponent's board on `\url{http://localhost:5000/own_board.html` and `\url{http://localhost:5000/opponent_board.html` respectively.
It is up to you how you visually represent the state of each board.


## BONUS

I will award __one bonus point__ for each of the following:  

* The group with the most visually appealing representation of game boards.

* Any group that eliminates the need for client.py in favor of using a browser client. 
  *Hint: Think about how to update files by replacing them*

* Any group that implements the Version 1 rules of the [Battleship: Advanced Missions](https://en.wikipedia.org/wiki/Electronic_Battleship:_Advanced_Mission) variant of the game.



## What to Submit

* \[2 points\] Find a partner.
Submit `partners.txt` with your partner's, or partners' first and last name.

* \[20 points\] `server.py` and `client.py` -- your working Python implementation of your server process. 
A YouTube video link showing the execution of your program.
Videos must be under 5 minutes in length - videos longer than that will not be graded.

* \[1 points\] (BONUS) `bonus1.png` -- a screenshot of the browser showing the visual representation of your board.

* \[1 points\] (BONUS) `bonus2.js` -- your working implementation of a browser client.
A YouTube video link showing the execution of your program.

* \[1 points\] (BONUS) `client_am.py` and `server_am.py` -- implementing the Advanced Missions rules of the Battleship game.
A YouTube video link showing the execution of your program.


## Grading Rubric

I will grade your submissions of the basic Battleship program from the YouTube video as follows:

* \[2 points\] `server.py` shows the initial representation of player's own board
* \[2 points\] `server.py` shows the initial representation of opponent's board
* \[3 points\] `client.py` sends a correctly formatted `fire` message (may be shown in Wireshark)
* \[5 points\] `server.py` correctly processes the `fire` message to update `own_board.txt`. Make sure to show all possible cases.
* \[3 points\] `server.py` sends a correctly formatted `response` message (may be shown in Wireshark)
* \[5 points\] `client.py` correctly processes the `result` message to update `opponent_board.txt`. Make sure to show all possible cases.



