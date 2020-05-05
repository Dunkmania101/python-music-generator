from random import randint as rint
from time import sleep
from mingus.midi import fluidsynth

# ----------
# Path to sf2 file (Do not output sound if empty string):
sf2 = ""
# Default pack installed with fluidsynth:
sf2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

# Tell what sound driver to use for the sf2 sound
# ("alsa" may be needed for linux users)
# Leave string empty for system default:
sound_driver = "alsa"

# Set to the desired time between / length of notes in seconds:
seconds = 0.3

# Set to the desired number of phrases:
stop_point = 10

# Set to the desired pitch multiplier (greater value = greater pitch, lowest is 1)
# Odd numbers seem to make it sound a bit less like horror music (:
multiplier = 15

# Set to the desired velocity when playing notes:
velocity = 100
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
notes = [rint(1, 6)]
notes.append(int(notes[-1]*rint(4, 6)))
len_phrase = rint(6, 18)
for l1 in range(0, stop_point):
    if len(notes) > len_phrase:
        if rint(1, 2) == 1:
            phrase_start = int((len(notes)/len_phrase)*rint(1, int(len(notes)/len_phrase)))
            phrase_end = int((len(notes)/len_phrase)*(rint(1, int(len(notes)/len_phrase))+1))
            phrase_notes = notes[phrase_start:phrase_end]
            for app_notes in phrase_notes:
                notes.append(app_notes)
    for compose in range(0, len_phrase+1):
        if notes[-1] < 2:
            notes.append(notes[-1]+1)
        if notes[-1] > rint(12, 24):
            notes.append(int(notes[-rint(1, 2)]/rint(4, 6)))
        else:
            notes.append(int(notes[-rint(1, 2)]*rint(4, 6)))
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
        fluidsynth.play_Note(play*multiplier, 0, velocity),
        fluidsynth.play_Note(play*multiplier/rint(2, 3), 0, velocity)
        sleep(seconds)
