# Python Music Generator

A Python script that randomly generates "music"

This is achieved by the following 5 step plan:
~~1. Pick a random starting note and add it to a list.~~
~~2. Add another random note for step #4.~~
~~3. Loop through step #4 for the number of notes needed in the piece.~~
~~4. Multiply one of the last few generated notes by a random ammount such that~~
~~the result is a multiple of 2 or 3 steps away from the previous and add~~
~~the result to the list.~~
~~5. Do some output with the list.~~

It used to work that way. Now it does this:
1. Pick a random starting note and add it to a list.
2. Pick a random time signature.
3. Add another note in the same scale as the first to the list.
4. Repeat step #2 until the time signature is reached for the current bar.
5. Repeat from step #1 until the set length is reached.


The actual mechanism is a bit more complex. For example, that list does not include its phrase system,
where it occasionally repeats previous segments for better sounding music.


There are a few parameters that can be changed at the top of the "musicgen.py" file.
These include the length of the piece, some modifiers for the notes and settings for the sound system.


It plays through PyAudio and can create .wav files.
Feel free to change the sound output system if you need / want something else.


There are sample wave outputs in the "sample_songs" folder.
The one with the greatest number at the end is the newest, although there may have been smaller udpades to the script since.

When running the commands below, be sure not to include the "$".



__Installing Dependencies ==>__

For Debian / Ubuntu:
$ sudo apt install python3 python3-pip python3-all-dev portaudio19-dev python3-pyaudio
$ sudo apt install git (Only needed if cloning)

For other distributions:
Use your package manager to install __python3 python3-pip python3-all-dev portaudio19-dev python3-pyaudio (Optional:) git__ or equivalent.


If these steps don't work for / apply to you, refer to [Python's installation page](https://www.python.org/downloads/ "Python's installation page") and / or [PyAduio's installation page](https://people.csail.mit.edu/hubert/pyaudio/ "PyAduio's installation page")



__Usage ==>__

1. If needed, install the required dependencies as shown above.
2. Download at least the "musicgen.py" file to the desired location for running. You can also clone this entire repository with:
$ git clone https://github.com/Dunkmania101/python-music-generator.git
3. If you wish to change some settings, edit the variables at the top of the downloaded "musicgen.py" file.
4. From the directory the file is in, run the command:
$ python3 musicgen.py
5. Enjoy!


Also, I don't drink coffee ;)