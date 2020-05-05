from random import randint as rint
# ----------
# Path to sf2 file (Do not output sound if empty string):
out_sound = True


# Set to the desired number of phrases:
stop_point = 50


# Set to the desired time between / length of notes in seconds:
seconds = 1


# Set to the desired pitch multiplier (greater value = greater pitch, lowest is 1):
multiplier = 24


# Whether to output lots of details or just the notes:
verbose = False
# ----------


# ----------
# Prevent breakage from user error in parameters:
stop_point = int(stop_point)
multiplier = int(multiplier)
# ----------


# ----------
# Main mechanism:
def rep_phrase():
    if len(notes) >= len_phrase:
        if rint(1, 2) == 1:
            if verbose:
                print(f"len(notes) = {len(notes)}")
            phrase_pos = rint(1, len(notes)/len_phrase)
            phrase_start = phrase_pos*len_phrase
            phrase_end = (phrase_pos+1)*len_phrase
            phrase_notes = notes[phrase_start:phrase_end]
            if verbose:
                print(f"Repeated phrase at {phrase_start}:{phrase_end}, containing {phrase_notes}")
            for app_notes in phrase_notes:
                notes.append(app_notes)


def mkcompose():
    if notes[-1] < 2:
        notes[-1] += 1
    if notes[-1] > rint(12, 24):
        notes.append(int(notes[-rint(1, 2)]/rint(2, 3)))
    else:
        notes.append(int(notes[-rint(1, 2)]*rint(2, 3)))


notes = [rint(1, 12)]
notes.append(notes[-1]*rint(4, 6))
len_phrase = rint(6, 18)
if verbose:
    print(f"len_phrase = {len_phrase}")
for initcompose in range(2, len_phrase):
    mkcompose()

for compose in range(1, stop_point):
    rep_phrase()
    for lmkcompose in range(0, len_phrase):
        mkcompose()
for index, note in enumerate(notes):
    notes[index] *= multiplier
print(f"final notes (numerical) = {notes}")
# ----------


# ----------
# This part prints out the actual musical notes
# instead of the ugly numbers.
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

key_out = []
for out in notes:
    if out in keys:
        key_out.append(keys[out])
    else:
        octave = int(out/12)
        key_out.append(f"{keys[out+1-(octave*12)]} oct. {octave}")
print(f"final notes (normal) = {key_out}")
# ----------


# ----------
# Play result if enabled
if out_sound:
    import pyaudio
    import numpy as np
    p = pyaudio.PyAudio()
    volume = 1     # range [0.0, 1.0]
    sr = 44100
    freq = 440.0        # sine frequency, Hz, may be float
    samples = []
    for app_samples in notes:
        samples.append(np.sin(2*np.pi*np.arange(sr*seconds)*app_samples/sr).astype(np.float32))
    for play in samples:
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=sr,
                        output=True)
        stream.write(volume*play)
        stream.stop_stream()
        stream.close()
    p.terminate()
# ----------
