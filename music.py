# ----------
# Set to "True" for piano sound
# Set to "False" for sine-wave sound
piano = True

# Set to the desired time between / length of notes
seconds = 0.3
# ----------


from random import randint as rint
if piano:
    from mingus.midi import fluidsynth
    fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2', "alsa")
    import time
else:
    import numpy as np
    import simpleaudio as sa


keys = {
    1: "c",
    2: "c#",
    3: "d",
    4: "d#",
    5: "e",
    6: "f",
    7: "f#",
    8: "g",
    9: "g#",
    10: "a",
    11: "a#",
    12: "b"
}

notes = [rint(1, 12)]
notes.append((notes[-1]*rint(2, 3)))
notes.append(int(notes[-1]/rint(2, 3)))
for l1 in range(0, 1000):
    if notes[-1] < 2:
        notes[-1] += 1
    if notes[-1] > 6:
        notes.append(int(notes[-rint(1, 3)]/rint(2, 3)))
    elif notes[-1] < 5:
        notes.append(int(notes[-rint(1, 3)]*rint(2, 3)))
    else:
        if rint(1, 2) == 1:
            notes.append(int(notes[-rint(1, 3)]*rint(2, 3)))
        else:
            notes.append(int(notes[-rint(1, 3)]/rint(2, 3)))
print(notes)

lout = []
for out in notes:
    if out in keys:
        lout.append(keys[out])
    else:
        octave = int(out/12)
        lout.append(f"{keys[out+1-(octave*12)]} oct. {octave}")
print(lout)


if piano:
    for play in notes:
        if play < 50:
            fluidsynth.play_Note(play*5, 0, 100)
        else:
            fluidsynth.play_Note(play*2, 0, 100)
        time.sleep(seconds)
else:
    a = 2**(1/12)
    fs = 44100
    for play in notes:
        frequency = 261.63*(a**play)
        t = np.linspace(0, seconds, seconds * fs, False)
        note = np.sin(frequency * t * 2 * np.pi)
        audio = note * (2**15 - 1) / np.max(np.abs(note))
        audio = audio.astype(np.int16)
        play_obj = sa.play_buffer(audio, 1, 2, fs)
        play_obj.wait_done()
