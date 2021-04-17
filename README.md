# Python Controller for Blackmagic Design Hyperdeck
### Harnessing the HyperDeck's "Blackmagic HyperDeck Ethernet Protocol"

This repo has a simple Python3 program that:
* Lists clips on a HyperDeck slot disk / SD card
* Allows you to choose a clip to play
* Alternatively, allows you to enter a start and end timecode

The purpose of this repository is to get you started creating Python control scripts for the HyperDeck.
The use I have is for building a controlled playlist for playout in a livestream, where the clips are
not necessarily in the correct order on the disk, and some clips (for example channel idents) will play frequently,
in between other 'program' clips.

This is a work in progress so be free to join in. My main objective is to wrap the protocol commands in 
Python functions within the 'HyperDeck' class included with this repo.

The underlying communication with the Hyperdesk is over a simple internal network connection using the 
built-in Python 'socket' library. 
In turn, a Python web server provides an API to access HyperDeck and now DataClip (playlist)
functions.
### FAST START ###
1. Make sure your BlackMagic HyperDeck is switched on and can be seen over your local network.
2. From a terminal prompt, replacing '192.168.0.145' with your HyperDeck's IP address: <pre>python webserver.py 192.168.0.145</pre>
3. Open a web browser and head to: http://localhost:8080