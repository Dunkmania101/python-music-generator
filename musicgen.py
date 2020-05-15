from random import randint as rint
# ----------
# Whether to output sound (Leave empty string for none)
# (Set to False to reduce wait time for wav file):
out_sound = True


# Path to output / name of wav file (Leave empty string to disable):
out_wav = ""
# out_wav = "sample_songs/out2.wav"


# Whether to use a sine triangle (Use a sine wave if False):
triangle = False


# Whether to output lots of details or just the notes:
verbose = False


# Set to the desired number of phrases:
stop_point = 30


# Set to the desired pitch multiplier (greater value = greater pitch, lowest is 1):
pitch_multiplier = 1


# Set to the desired BPM:
bpm = 360


# Volume (0.x for lower, x.x for higher, 1.0 is default):
volume = 1.0


# Whether to keep notes within a reasonable range:
fix_pitch = True


# Range of acceptable note speeds ( = None for no limit):
fix_speed_max = 4
fix_speed_min = 1
# ----------


# ----------
# Prevent breakage from user error in parameters, where possible:
stop_point = int(stop_point)
pitch_multiplier = int(pitch_multiplier)
bpm = int(bpm)
# ----------


# ----------
# Main mechanism:
def mk_compose(note_in):
    if note_in < 2:
        note_in += 2
    if note_in > 12:
        return(int(note_in/rint(3, 5)))
    else:
        return(int(note_in*rint(3, 5)))


def run_mk_compose():
    if len(notes[-1]) < len_phrase:
        if sum([b[-1] for b in notes[-1][-1]]) < sig[0] and len(notes[-1][-1]) > 0:
            notes[-1][-1].append([mk_compose(notes[-1][-1][-1][0]), rint(1, sig[0]-sum([b[1] for b in notes[-1][-1]]))])
        else:
            notes[-1].append([[mk_compose(notes[-1][-1][-1][0]), rint(1, sig[0])]])
    else:
        notes.append([[[mk_compose(notes[-1][-1][-1][0]), rint(1, sig[0])]]])


def rep_bar():
    notes.append(notes[-1][0:-rint(1, int(len(notes[-1])/2))])


sig = [rint(2, 12), 2**rint(1, 4)]
notes = [[[[int(rint(1, 12)*1.5), rint(1, sig[0])]]]]
len_phrase = rint(6, 12)
if verbose:
    print(f"Length of each phrase: {len_phrase}")
    print(f"Time signature: {sig}")
for linit_compose in range(1, len_phrase):
    run_mk_compose()
    if verbose:
        print(f"Added note: {notes[-1][-1][-1][0]} for {notes[-1][-1][-1][1]} beat(s)")
for lcompose in range(1, stop_point):
    rep_bar()
    if rint(1, 4) == 1:
        notes.append(notes[rint(0, len(notes)-1)])
        if verbose:
            print(f"Repeated phrase at {len(notes)-1}, containing {notes[-1]}")
            print(f"Number of phrases: {len(notes)}")
    run_mk_compose()
    if verbose:
        print(f"Added note: {notes[-1][-1][-1][0]} for {notes[-1][-1][-1][1]} beat(s)")


if fix_pitch:
    for index, lfix_pitch in enumerate(notes):
        for index1, lfix_pitch1 in enumerate(lfix_pitch):
            for index2, lfix_pitch2 in enumerate(lfix_pitch1):
                while notes[index][index1][index2][0] < 24:
                    notes[index][index1][index2][0] *= 2
                while notes[index][index1][index2][0] > 60:
                    notes[index][index1][index2][0] /= 2


for index, lmultiply in enumerate(notes):
    for index1, lmultiply1 in enumerate(lmultiply):
        for index2, lmultiply12 in enumerate(lmultiply1):
            notes[index][index1][index2][0] *= pitch_multiplier
print("----------")
print(f"Key signature: {sig[0]}/{sig[1]}")
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
    for out1 in out:
        for out2 in out1:
            if out2[0] in keys:
                key_out.append(f"{keys[out2[0]]} in octave 1 for {out2[1]} beats.")
            else:
                octave = int(out2[0]/12)
                key_out.append(f"{keys[out2[0]-(octave*12)]} in octave {octave+1} for {out2[1]} beats.")
print("----------")
print(f"Key signature: {sig[0]}/{sig[1]}")
print(f"Final notes (normal): {key_out}")
print("----------")
# ----------


# ----------
# Output result if enabled:
if out_sound or out_wav != "":
    import numpy as np
    import pyaudio
    if triangle:
        from scipy import signal
    sr = 44100
    samples = []
    for app_samples in notes:
        for app_samples1 in app_samples:
            for app_samples2 in app_samples1:
                freq = 27.5*(2**(app_samples2[0]/12))
                if triangle:
                    t = np.linspace(0, app_samples2[1]*(60/bpm), sr*app_samples2[1])
                    samples.append(signal.sawtooth(2 * np.pi * t * freq, width=0.5).astype(np.float32))
                else:
                    samples.append(np.sin(2*np.pi*np.arange(sr*app_samples2[1]*(60/bpm))*freq/sr).astype(np.float32)*volume)
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
    if out_wav != "":
        import wave
        wf = wave.open(out_wav, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
        wf.setframerate(sr)
        wf.writeframes(b''.join(samples))
        wf.close()
    p.terminate()
# ----------
