from random import randint as rint
from time import sleep
from mingus.midi import fluidsynth

# ----------
# Path to sf2 file (Do not output sound if empty string):
sf2 = ""
# Default pack installed with fluidsynth:
# sf2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

# Tell what sound driver to use for the sf2 sound
# ("alsa" may be needed for linux users)
# Leave string empty for system default:
sound_driver = ""

# Set to the desired time between / length of notes in seconds:
seconds = 0.3

# Set to the desired number of notes:
stop_point = 100
# ----------


if sf2 != "" and sound_driver != "":
    fluidsynth.init(sf2, sound_driver)
elif sf2 != "" and sound_driver == "":
    fluidsynth.init(sf2)
elif sf2 == "" and sound_driver != "":
    fluidsynth.init(None, sound_driver)
elif sf2 == "" and sound_driver == "":
    fluidsynth.init(None)


# ----------
# Main mechanism:
notes = [rint(1, 12)]
notes.append((notes[-1]*rint(4, 6)))
notes.append(int(notes[-1]/rint(4, 6)))
for l1 in range(0, stop_point):
    if notes[-1] < 2:
        notes[-1] += 1
    if notes[-1] > 6:
        notes.append(int(notes[-rint(1, 3)]/rint(4, 6)))
    elif notes[-1] < 5:
        notes.append(int(notes[-rint(1, 3)]*rint(4, 6)))
    else:
        if rint(1, 2) == 1:
            notes.append(int(notes[-rint(1, 3)]*rint(4, 6)))
        else:
            notes.append(int(notes[-rint(1, 3)]/rint(4, 6)))
print(notes)
# ----------


# This part is supposed to print out the actual musical notes
# instead of the ugly numbers.
# Broken for now...
# keys = {
#     1: "c",
#     2: "c#",
#     3: "d",
#     4: "d#",
#     8: "g",
#     9: "g#",
#     10: "a",
#     11: "a#",
#     12: "b"
# }
#
# lout = []
# for out in notes:
#     if out in keys:
#         lout.append(keys[out])
#     else:
#         octave = int(out/12)
#         lout.append(f"{keys[out+1-(octave*12)]} oct. {octave}")
# print(lout)

if sf2 != "":
    for play in notes:
        if play < 15:
            fluidsynth.play_Note(play*5, 0, 100)
        else:
            fluidsynth.play_Note(play*2, 0, 100)
        sleep(seconds)
