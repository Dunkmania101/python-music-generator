# Python Music Generator

A Python script that randomly generates "music"

This is achieved by the following 5 step plan:
1. Pick a random starting note and add it to a list.
2. Add another random note for step 4.
3. Loop through step 4 for the number of notes needed in the piece.
4. Multiply one of the last few generated notes by a random ammount such that
the result is a multiple of 2 or 3 steps away from the previous and add
the result to the list.
5. Do some output with the list.

The actual mechanism is a bit more complex. For example, that list does not include its phrase system,
where it occasionally repeats previous segments for better sounding music. It also leaves out the time signature system,
used for better song structure.


There are a few parameters that can be changed at the top of the "musicgen.py" file.
These include the length of the piece, some modifiers for the notes and settings for the sound system.


It plays through PyAudio and can create .wav files.
Feel free to change the sound output system if you need / want something else.


There are sample wave outputs in the "sample_songs" folder.
The one with the greatest number at the end is the newest, although there may have been smaller udpades since.

__Installing Dependencies ==>__

For Debian / Ubuntu:
$ sudo apt install python3 python3-pip python3-all-dev portaudio19-dev python3-pyaudio

For other distributions:
Use your package manager to install __python3 python3-pip python3-all-dev portaudio19-dev python3-pyaudio__

Finally:
$ pip3 install pyaudio scipy

If these steps don't work for you, refer to [PyAduio's installation page](https://people.csail.mit.edu/hubert/pyaudio/ "PyAduio's installation page") and / or [Python's installation page](https://www.python.org/downloads/ "Python's installation page") and / or [SciPy's installation page](https://www.scipy.org/install.html "SciPy's installation page")