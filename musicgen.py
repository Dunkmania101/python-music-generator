from random import randint as rint
# ----------
# Whether to output sound (Leave empty string for none)
# (Set to False to reduce wait time for wav file):
out_sound = True


# Path to output wav file (Leave empty string for none):
out_wav = ""
# out_wav = "sample_songs/out1"


# Whether to use a sine triangle (Use a sine wave if False):
triangle = False


# Whether to output lots of details or just the notes:
verbose = False


# Set to the desired number of phrases:
stop_point = 15


# Set to the desired pitch multiplier (greater value = greater pitch, lowest is 1):
pitch_multiplier = 1


# Set to the desired speed multiplier:
speed_multiplier = 4


# Volume (0.x for lower, x.x for higher, 1.0 is default):
volume = 1.0


# Whether to keep notes within the range of an 88-key piano:
fix_pitch = True


# Range of acceptable note speeds (None for no limit):
fix_speed_max = 4
fix_speed_min = 1
# ----------


# ----------
# Prevent breakage from user error in parameters, where possible:
stop_point = int(stop_point)
pitch_multiplier = int(pitch_multiplier)
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


def mk_compose():
    if verbose:
        print(f"Last note added: {notes[-1][0]}")
    if notes[-1][0] < 2:
        notes[-1][0] += 1
    note_select = rint(1, 2)
    if notes[-note_select][0] > rint(6, 12):
        notes.append([int(notes[-note_select][0]/rint(2, 3))])
    else:
        notes.append([int(notes[-note_select][0]*rint(2, 3))])
    notes[-1].append(notes[-1][0]/3)


notes = [[rint(1, 12)]]
notes[-1].append(notes[-1][0]/3)
notes.append([int(notes[-1][0]*rint(2, 3))])
notes[-1].append(notes[-1][0]/3)
len_phrase = rint(6, 24)
if verbose:
    print(f"Length of each phrase: {len_phrase}")
for linit_compose in range(2, len_phrase):
    mk_compose()

for lcompose in range(1, stop_point):
    rep_phrase()
    for lmkcompose in range(0, len_phrase):
        mk_compose()


if fix_pitch:
    for index, lfix_pitch in enumerate(notes):
        while notes[index][0] > 88:
            notes[index][0] /= 2


if fix_speed_max is not None:
    for index, lfix_speed_max in enumerate(notes):
        while notes[index][1] > fix_speed_max:
            notes[index][1] /= 2


if fix_speed_min is not None:
    for index, lfix_speed_min in enumerate(notes):
        while notes[index][1] < fix_speed_min:
            notes[index][1] *= 2


for index, lnote in enumerate(notes):
    notes[index][0] *= pitch_multiplier
    notes[index][1] /= speed_multiplier
print("----------")
print(f"Final notes (numerical): {notes}")
print("----------")
# ----------


# ----------
# This part prints out the actual musical notes
# instead of the ugly numbers:
keys = {
    0: "a",
    1: "a#",
    2: "b",
    3: "c",
    4: "c#",
    5: "d",
    6: "d#",
    7: "e",
    8: "f",
    9: "f#",
    10: "g",
    11: "g#"
}

key_out = []
for out in notes:
    if out[0] in keys:
        key_out.append(f"{keys[out[0]]} in octave 1 for {out[1]} sec.")
    else:
        octave = int(out[0]/12)
        key_out.append(f"{keys[out[0]-(octave*12)]} in octave {octave+1} for {out[1]} sec.")
print("----------")
print(f"Final notes (normal): {key_out}")
print("----------")
# ----------


# ----------
# Output result if enabled:
if out_sound or out_wav != "":
    import numpy as np
    import pyaudio
    sr = 44100
    samples = []
    for app_samples in notes:
        freq = 27.5*(2**(app_samples[0]/12))
        if triangle:
            from scipy import signal
            t = np.linspace(0, app_samples[1], sr*app_samples[1])
            samples.append(signal.sawtooth(2 * np.pi * t * freq, width=0.5).astype(np.float32))
        else:
            samples.append(np.sin(2*np.pi*np.arange(sr*app_samples[1])*freq/sr).astype(np.float32)*volume)
        p = pyaudio.PyAudio()
if out_sound:
    from time import sleep
    for play in samples:
        stream = p.open(format=pyaudio.paFloat32, channels=1, rate=sr, output=True)
        if verbose:
            print(play)
        stream.write((play).tobytes())
        stream.stop_stream()
        sleep(0.02)
        stream.close()
    p.terminate()
if out_wav != "":
    import wave
    wf = wave.open(out_wav + ".wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
    wf.setframerate(sr)
    wf.writeframes(b''.join(samples))
    wf.close()
# ----------
