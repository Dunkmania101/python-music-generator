# Python Music Generator

A Python script that randomly generates "music"

This is achieved by the following 5 step plan:
1. Pick a random starting note and add it to a list.
2. Add two other random notes for step 4.
3. Loop through step 4 for the number of notes needed in the piece.
4. Multiply one of the last few generated notes by a random ammount such that
the result is a multiple of 2 or 3 steps away from the previous and add
the result to the list.
5. Do some output with the list.


It plays through Fluidsynth with an sf2 pack.
Feel free to change the output system if you need / want something else.

__Installing Dependencies ==>__

For ubuntu:
$ sudo apt install python3 python3-pip fluidsynth 

For other distributions:
Use your package manager to install __python3 python3-pip fluidsynth__

Finally:
$ pip3 install mingus
