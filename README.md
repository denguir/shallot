# shallot

How to use
----------
This program allows the user to establish an encrypted TCP/IP connection between
a Sender and a Receiver. The messages sent by the Sender walk through a network
composed of many relays untill reaching the Receiver. The topology of the network
can be built in the config file topology.ini. In the config files host_R?.ini,
each node of the network is attributed a given IP address and port number.

To test the program, go to example folder and run first Relay1.py, Relay2.py
and BoB.py, each in a different terminals. Then run Alice.py also
in a different terminal. Alice should be able to send any message to Bob.py
