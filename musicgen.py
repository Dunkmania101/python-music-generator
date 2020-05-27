from random import randint as rint
# ----------
# Config:
# ----------
# Whether to output sound (Leave the string empty for none)
# (Set to False to reduce wait time for wav file):
out_sound = True


# Path to output / name of wav file (Leave the string empty to disable)
# Ensure any folders already exist but the wave file does not!:
out_wav = ""
# out_wav = "sample_songs/out6.wav"


# Whether to output lots of details or just the notes (True or False):
verbose = False


# Set to the desired number of phrases:
stop_point = 15


# Set to the desired pitch multiplier (greater value = greater pitch; lowest is 1)
# CURRENTLY ANYTHING GREATER THAN TWO(2) IS INSANELY HIGH PITCHED!!!:
pitch_multiplier = 2


# Set to the desired playback BPM:
bpm = 120


# Volume (0.x for lower, x.x for higher, 1.0 is default):
volume = 0.5


# Whether to keep notes within a reasonable range (True or False)
# This setting is typically not needed when pitch_multiplier < 2:
fix_pitch = False
# End Of Config
# ----------


# ----------
# Prevent breakage from user error in parameters, where possible:
stop_point = int(stop_point)
pitch_multiplier = int(pitch_multiplier)
bpm = int(bpm)
# ----------


# ----------
# Main mechanism:
def first_note():
    return notes[0][0][0][0]


def last_note():
    return notes[-1][-1][-1][-1]


def last_bar():
    return notes[-1][-1]


def mk_compose():
    last_bar()[0].append([scale[rint(1, 7)]])
    last_note().append(int(sig[0]/last_note()[0]/2)+1)
    if last_bar()[0].count(-1) < len(last_bar()[0])/1.5:
        last_bar()[0].append([-1])
        last_note().append(int(sig[0]/last_bar()[0][-2][0]/3)+1)


def mk_compose_ud():
    if up_down == 1:
        last_bar()[0].append([scale[rint(4, 7)]])
    else:
        last_bar()[0].append([scale[rint(1, 4)]])
    last_note().append(int(sig[0]/last_note()[0]/2)+1)


sig = [rint(9, 18), 2**rint(1, 4)]
notes = [[[[[rint(24, 36)]]]]]
last_note().append(int(sig[0]/last_note()[0]/2))
while len(notes) < stop_point:
    if rint(1, 2) == 1:
        scale = {
            1: first_note()[0]+2,
            2: first_note()[0]+2,
            3: first_note()[0]+3,
            4: first_note()[0]+5,
            5: first_note()[0]+7,
            6: first_note()[0]+9,
            7: first_note()[0]+10
        }
    else:
        scale = {
            1: first_note()[0]+2,
            2: first_note()[0]+3,
            3: first_note()[0]+5,
            4: first_note()[0]+7,
            5: first_note()[0]+8,
            6: first_note()[0]+10,
            7: first_note()[0]+12
        }
    while sum([b[1] for b in last_bar()[0]]) < sig[0]/2:
        mk_compose()
    last_bar().append(last_bar()[0])
    up_down = rint(1, 2)
    while sum([b[1] for b in last_bar()[0]]) < sig[0]:
        mk_compose_ud()
    notes.append([[[[first_note()[0]]]]])
    last_note().append(int(sig[0]/last_note()[0]/2))


if fix_pitch:
    for index, lfix_pitch in enumerate(notes):
        for index1, lfix_pitch1 in enumerate(lfix_pitch):
            for index2, lfix_pitch2 in enumerate(lfix_pitch1):
                for index3, lfix_pitch3 in enumerate(lfix_pitch2):
                    if lfix_pitch3[0] != -1:
                        while notes[index][index1][index2][index3][0] < 24:
                            notes[index][index1][index2][index3][0] += 12
                        while notes[index][index1][index2][index3][0] > 48:
                            notes[index][index1][index2][index3][0] -= 12


if pitch_multiplier > 1:
    for index, lmultiply in enumerate(notes):
        for index1, lmultiply1 in enumerate(lmultiply):
            for index2, lmultiply2 in enumerate(lmultiply1):
                for index3, lmultiply3 in enumerate(lmultiply2):
                    if lmultiply3[0] != -1:
                        notes[index][index1][index2][index3][0] += int(12*(pitch_multiplier-1))
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
for index, out in enumerate(notes):
    key_out.append(f"||")
    key_out.append(f"Phrase {index}: ")
    for out1 in out:
        for index1, out2 in enumerate(out1):
            key_out.append("--")
            key_out.append(f"Bar {index}: ")
            for out3 in out2:
                if out3[0] == -1:
                    key_out.append(f"Rest for {out3[1]} beats.")
                else:
                    if out3[0] in keys:
                        key_out.append(f"{keys[out3[0]]} in octave 1 for {out3[1]} beats.")
                    else:
                        octave = int(out3[0]/12)
                        key_out.append(f"{keys[out3[0]-(octave*12)]} in octave {octave+1} for {out3[1]} beats.")
            key_out.append("--")
    key_out.append(f"||")
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
    sr = 44100
    samples = []
    save_volume = volume
    for app_samples in notes:
        for app_samples1 in app_samples:
            for app_samples2 in app_samples1:
                for app_samples3 in app_samples2:
                    if app_samples3 == -1:
                        volume = 0
                    else:
                        freq = 27.5*(2**(app_samples3[0]/12))
                    samples.append(
                        np.sin(2*np.pi*np.arange(sr*app_samples3[1]*(60/bpm))*freq/sr)
                        .astype(np.float32)*volume)
                    volume = save_volume
    p = pyaudio.PyAudio()
    if out_sound:
        from time import sleep
        for index, play in enumerate(samples):
            if verbose:
                print(f"Playing note {index+1} of {len(samples)+1} which is sample:")
                print(play)
            stream = p.open(format=pyaudio.paFloat32,
                            channels=1,
                            rate=sr,
                            output=True)
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
print("Done!")
print(f"I wrote {len(notes)} phrases,")
print(f"{sum([sum([len(b) for b in p]) for p in notes])} bars,")
print(f"and {sum([sum([len([sum([len(n) for n in b]) for p in notes]) for b in p]) for p in notes])} notes!")
print("Exiting...")
# ----------
