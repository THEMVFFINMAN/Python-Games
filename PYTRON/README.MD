# PyTron
======

A pygame project based on the lightcycle games for Tron. While it is mostly working, I am working on developing extremely good AI.

While the game is relatively efficient and fast, I am also looking for ways to make it increasingly faster. 

## Implementation 

Currently the board is represented by a strongly connected undirected graph using a dict data structure. 
Each coordinate is represented by a tuple as a key in the dict. 
And each coordinate key points to a list of tuples of the coordinates it is next to.
Every time a block of the driver's tail is created, that key and its neighbors who contain that key's value, are removed from the dict.
If a driver hits a coordinate not in the dict, then it crashed and the game resets. 


## AI

My favorite. Currently this is how the AI works. There are a few steps. Because the graph is represented using a dict, 
getting a coord at any given time is constant time. Knowing this, every step of the way the AI driver checks each direction 
using a flood fill algorithm. So if it's going right, it gets the coordinate to the top, right, and bottom. It then adds them all 
and their neighbors to a counter. It then returns the counter. It finds which side has the largest number of free blocks, and goes that way. 

On top of this, I use a "future" graph instead of the graph of the current board. Basically the user driver emits a line in front of them 
and to both sides. To demonstrate this, I uploaded a few images. 

The first image depicts the enemy driver having to make a decision vs the user driver based on the AI. 
As you can see, the user driver is emitting an invisible line to its front, and sides which the AI sees. 
So when it runs the flood fill, it gets 4 to its left side, 0 to its front, and a bunch on its right so it chooses right.

![alt text](https://raw.githubusercontent.com/THEMVFFINMAN/Python-Games/master/PYTRON/image.png "AI1")

This next image shows a larger example of the previous example. The AI hits a wall and has to make a decision, go left or right. 
The AI can see that the left enclosure is smaller because the user driver's future trail is closing it up and so it will choose right. 

![alt text](https://raw.githubusercontent.com/THEMVFFINMAN/Python-Games/master/PYTRON/ai2.PNG "AI2")

Special checks have been put into place so that in the following image, the enemy AI can see the trap and choose to go down to avoid it. 

![alt text](https://raw.githubusercontent.com/THEMVFFINMAN/Python-Games/master/PYTRON/ai3.PNG "AI3")

But so that the user driver doesn't emit it wall in cases like the one below:

![alt text](https://raw.githubusercontent.com/THEMVFFINMAN/Python-Games/master/PYTRON/ai4.PNG "AI4")


## TODO
======

1. Actually implement score
2. Have AI work with multiple AI drivers instead of just the user
3. Delete the driver's tail on death to facilitate a multi driver game instead of just restart
4. Have AI maximize cling to walls when it knows that the user driver is not in its enclosure
5. Some sort of aggressive AI would be kind of nice
