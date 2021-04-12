# Python Controller for Blackmagic Design Hyperdeck
### Using the HyperDeck's "Blackmagic HyperDeck Ethernet Protocol"

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
built-in Python 'socket' library. I have also used PrettyTable in test.py to make the clips list look
nicer: <pre>pip install PrettyTable</pre>

To run the demo, put some clips on a card in your HyperDeck, set the IP address in test.js
and then (making sure you are using Python3):
<pre>python test.js</pre>

