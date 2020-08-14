from random import randint as rint

# ----------
# Config:
# ----------
# Whether to output sound (Set to False to reduce wait time for out_wav file, if applicable):
out_sound = True


# Path to sf2 file (Leave the string empty to disable, plays with sine wave if disabled):
sf2 = ""
# sf2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"


# Path to output / name of wav file (Leave the string empty to disable)
# Ensure any folders already exist but the wave file does not!:
out_wav = ""
# out_wav = "sample_songs/out9.wav"


# Whether to output the actual keys or just the numerical notes:
out_keys = True


# Whether to output lots of details or just the notes (True or False):
verbose = False


# Whether to print progress:
progress = True


# Set to the desired number of phrases:
stop_point = 14


# Set to the desired pitch multiplier (greater value = greater pitch; minimum is 1)
# CURRENTLY ANYTHING GREATER THAN ONE(1) IS INSANELY HIGH PITCHED!!!:
pitch_multiplier = 1


# Set to the desired speed multiplier (greater value = greater speed; minimum is 1):
speed_multiplier = 1


# Volume (0.x for lower, x.x for higher, 1.0 is default):
volume = 1


# Whether to keep notes within a reasonable range (True or False)
# This setting is typically not needed when pitch_multiplier < 2:
fix_pitch = True
# End Of Config
# ----------


# ----------
# Prevent breakage from user error in parameters, where possible:
stop_point = int(stop_point)
pitch_multiplier = int(pitch_multiplier)
# ----------


# ----------
# Main mechanism:
# -----
# Name Functions:
def beats_per_bar():
    return sig[0]


def first_note():
    return notes[0][0][0][0]


def last_bar():
    return notes[-1][-1]


def first_subbar():
    return last_bar()[0]


def last_subbar():
    return last_bar()[-1]


def first_last_note():
    return first_subbar()[-1]


def last_note():
    return last_subbar()[-1]


# Action Functions:
def pick_scale_first(scale_base):
    if min_maj == 1:
        if rint(1, 4) == 1:
            return first_note()[0] - scale[scale_base]
        else:
            return first_note()[0] + scale[scale_base]
    else:
        if rint(1, 4) == 1:
            return first_note()[0] + scale[scale_base]
        else:
            return first_note()[0] - scale[scale_base]


def pick_scale_ch_prog(scale_base):
    if min_maj == 1:
        if rint(1, 4) == 1:
            return ch_prog[count] - scale[scale_base]
        else:
            return ch_prog[count] + scale[scale_base]
    else:
        if rint(1, 4) == 1:
            return ch_prog[count] + scale[scale_base]
        else:
            return ch_prog[count] - scale[scale_base]


def app_beat():
    if int(beats_per_bar() / last_note()[0]) < 1 or len(notes) <= 1:
        return rint(1, 2)
    else:
        if int(beats_per_bar() / last_note()[0]) + sum([b[1] for b in last_subbar()]) > beats_per_bar():
            return abs(beats_per_bar() - sum([b[1] for b in last_subbar()]))
        else:
            return int(beats_per_bar() / last_note()[0])


def mk_compose():
    last_subbar().append([pick_scale_ch_prog(rint(1, 7)), app_beat()])
    if last_subbar().count(-1) < len(last_subbar())/1.5 and rint(1, 2) == 1:
        last_subbar().append([-1, app_beat()])


def mk_compose_ud(up_down):
    if up_down == 1:
        last_subbar().append([pick_scale_ch_prog(rint(4, 7)), app_beat()])
    else:
        last_subbar().append([pick_scale_ch_prog(rint(1, 4)), app_beat()])
    if last_subbar().count(-1) < len(last_subbar())/1.5 and rint(1, 2) == 1:
        last_subbar().append([-1, app_beat()])


def compose_phrase():
    global count
    count = 0
    while sum([b[1] for b in last_subbar()]) < beats_per_bar():
        mk_compose()
        count += 1
        if count > len(ch_prog) - 1:
            count = 0
    up_down = rint(1, 2)
    count = 0
    while sum([b[1] for b in last_subbar()]) < beats_per_bar():
        mk_compose_ud(up_down)
        count += 1
        if count > len(ch_prog):
            count = 0
    for lvary in range(0, rint(0, 6)):
        last_bar().append(last_subbar()[0:int(len(last_subbar())/rint(1, 3))])
        up_down = rint(1, 2)
        while sum([b[1] for b in last_subbar()]) < sig[0]:
            mk_compose_ud(up_down)


# -----
# Actually run now:
sig = [rint(9, 18), 2**rint(1, 4)]
notes = [[[[[rint(30, 42)]]]]]
if int(beats_per_bar() / last_note()[0]) < 1 or len(notes) <= 1:
    last_note().append(rint(1, 2))
else:
    last_note().append(int(beats_per_bar() / last_note()[0]))
bpm = first_note()[0] * rint(6, 9)
if sf2 != "":
    bpm *= 2
if rint(1, 2) == 1:
    maj_chance = 4
else:
    maj_chance = 4
while len(notes) < stop_point:
    if rint(1, maj_chance) == 1:
        min_maj = 1
        scale = {
            1: 2,
            2: 2,
            3: 3,
            4: 5,
            5: 7,
            6: 9,
            7: 10
        }
    else:
        min_maj = 2
        scale = {
            1: 2,
            2: 3,
            3: 5,
            4: 7,
            5: 8,
            6: 10,
            7: 12
        }
    ch_prog = []
    for lch_prog in range(0, rint(1, 6)):
        ch_prog.append(pick_scale_first(rint(1, 7)))
    compose_phrase()
    if rint(1, 2) == 1:
        notes.append(notes[0])
    if rint(1, 2) == 1:
        notes.append(notes[rint(0, len(notes)-1)])
    if rint(1, 2) == 1:
        notes.append([[[[first_note()[0], app_beat()]]]])
    else:
        notes.append([[[[first_last_note()[0], app_beat()]]]])


if fix_pitch:
    for index, lrep_code in enumerate(notes):
        for index1, lrep_code1 in enumerate(lrep_code):
            for index2, lrep_code2 in enumerate(lrep_code1):
                for index3, lrep_code3 in enumerate(lrep_code2):
                    if notes[index][index1][index2][index3][0] != -1:
                        while notes[index][index1][index2][index3][0] < 24:
                            notes[index][index1][index2][index3][0] += 12
                        while notes[index][index1][index2][index3][0] > 60:
                            notes[index][index1][index2][index3][0] -= 12

if pitch_multiplier > 1:
    for index, lrep_code in enumerate(notes):
        for index1, lrep_code1 in enumerate(lrep_code):
            for index2, lrep_code2 in enumerate(lrep_code1):
                for index3, lrep_code3 in enumerate(lrep_code2):
                    if notes[index][index1][index2][index3][0] != -1:
                        notes[index][index1][index2][index3][0] += 12*(pitch_multiplier-1)

# Just for setting the output manually, not part of the main program:
# notes = [[[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[-1, 1], [60, 1], [-1, 1], [40, 1], [-1, 2], [43, 1], [45, 1], [47, 2], [-1, 2]], [[-1, 1], [60, 1], [-1, 1], [40, 2], [43, 2], [-1, 2], [43, 2], [-1, 2]], [[-1, 1], [60, 1], [-1, 1], [40, 2], [53, 1], [-1, 1], [53, 1], [-1, 2]], [[-1, 1], [60, 1], [-1, 1], [40, 2], [53, 1], [-1, 1], [53, 1], [-1, 2]], [[-1, 1], [60, 1], [-1, 1], [40, 2], [48, 2], [48, 1], [57, 1], [-1, 2]], [[-1, 1], [60, 1], [-1, 1], [40, 2], [48, 2], [43, 2], [-1, 2]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[-1, 1], [33, 1], [35, 1], [-1, 1], [36, 1], [-1, 2], [28, 2], [-1, 2]], [[-1, 1], [33, 1], [27, 2], [47, 1], [25, 2], [-1, 2], [47, 2]], [[-1, 1], [33, 1], [27, 2], [30, 1], [37, 2], [37, 1], [32, 1], [30, 1]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[-1, 2], [26, 1], [-1, 1], [45, 2], [-1, 1], [31, 2], [-1, 2]], [[-1, 2], [26, 1], [-1, 1], [45, 2], [-1, 1], [31, 2], [-1, 2]], [[-1, 2], [26, 1], [-1, 1], [45, 2], [-1, 1], [31, 2], [-1, 2]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[-1, 1], [33, 1], [35, 1], [-1, 1], [36, 1], [-1, 2], [28, 2], [-1, 2]], [[-1, 1], [33, 1], [27, 2], [47, 1], [25, 2], [-1, 2], [47, 2]], [[-1, 1], [33, 1], [27, 2], [30, 1], [37, 2], [37, 1], [32, 1], [30, 1]]]], [[[[-1, 2], [31, 2], [-1, 1], [29, 2], [25, 1], [19, 1], [-1, 2]], [[-1, 2], [31, 2], [-1, 1], [26, 1], [-1, 1], [31, 2], [-1, 2]], [[-1, 2], [31, 2], [-1, 1], [20, 1], [40, 1], [20, 1], [16, 2]]]], [[[[-1, 1], [47, 2], [-1, 2], [50, 1], [50, 2], [48, 2]], [[-1, 1], [47, 2], [47, 1], [-1, 2], [40, 2], [47, 2], [-1, 1]], [[-1, 1], [47, 2], [47, 1], [-1, 2], [40, 2], [47, 2], [-1, 1]], [[-1, 1], [47, 2], [47, 1], [52, 1], [-1, 2], [54, 2], [-1, 2]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[38, 1], [31, 1], [-1, 1], [26, 1], [29, 2], [-1, 1], [28, 1], [-1, 2]], [[38, 1], [31, 1], [-1, 1], [26, 1], [40, 2], [-1, 2], [28, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [21, 2], [45, 1], [21, 2], [21, 1], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [26, 1], [26, 1], [26, 2], [30, 1], [26, 1], [30, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]], [[38, 1], [31, 1], [-1, 1], [30, 2], [28, 1], [-1, 1], [30, 2], [-1, 1]]]], [[[[-1, 1]]]]]
# sig = [10, 4]
# bpm = 190

print("----------")
print(f"Final notes (numerical): {notes}")
print(f"Key signature: {sig[0]}/{sig[1]}")
print(f"BPM: {bpm}")
print("----------")
# ----------


# ----------
# This part prints out the actual musical notes
# instead of the ugly numbers:
if out_keys:
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
                key_out.append([])
                for out3 in out2:
                    if out3[0] == -1:
                        key_out[-1].append(f"Rest for {out3[1]} beats.")
                    else:
                        if out3[0] in keys:
                            key_out[-1].append(f"{keys[out3[0]]} in octave 1 for {out3[1]} beats.")
                        else:
                            octave = int(out3[0]/12)
                            key_out[-1].append(f"{keys[out3[0]-(octave*12)]} in octave {octave+1} for {out3[1]} beats.")
                key_out.append("--")
        key_out.append(f"||")
    print("----------")
    print(f"Key signature: {sig[0]}/{sig[1]}")
    print(f"Final notes (normal):")
    print(key_out)
    print("----------")
# ----------


# ----------
# Output result if enabled:
if out_sound or out_wav != "":
    from time import sleep
    import numpy as np
    if out_wav:
        import wave
    import pyaudio
    p = pyaudio.PyAudio()
    sr = 44100
    samples = []
    if sf2 != "":
        from mingus.midi import pyfluidsynth
        fs = pyfluidsynth.Synth(samplerate=sr)
        fsf2 = fs.sfload(sf2)
        fs.program_select(0, fsf2, 0, 0)
        for index, lrep_code in enumerate(notes):
            for index1, lrep_code1 in enumerate(lrep_code):
                for index2, lrep_code2 in enumerate(lrep_code1):
                    for index3, lrep_code3 in enumerate(lrep_code2):
                        if lrep_code3[0] != -1:
                            fs.noteon(0, lrep_code3[0], volume*100)
                        samples.append(pyfluidsynth.raw_audio_string(np.array(fs.get_samples(int((sr * lrep_code3[1] * (60/bpm)) / speed_multiplier)))))
                        if lrep_code3[0] != -1:
                            fs.noteoff(0, lrep_code3[0])
        fs.delete()

    if sf2 == "":
        for index, lrep_code in enumerate(notes):
            for index1, lrep_code1 in enumerate(lrep_code):
                for index2, lrep_code2 in enumerate(lrep_code1):
                    for index3, lrep_code3 in enumerate(lrep_code2):
                        if lrep_code3[0] == -1:
                            freq = 0
                        else:
                            freq = 27.5*(2**(lrep_code3[0]/12))
                        samples.append((
                            np.sin(2*np.pi*np.arange(int((sr*lrep_code3[1]*(60/bpm) / speed_multiplier)))
                                    * freq/sr)
                            .astype(np.float32)*volume).tobytes()
                            )

    if out_sound:
        if sf2 == "":
            stream = p.open(format=pyaudio.paFloat32,
                            channels=2,
                            rate=sr,
                            output=True)
        else:
            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=sr,
                            output=True)
        for index, play in enumerate(samples):
            if progress:
                print(f"Playing note {index+1} of {len(samples)}")
            if verbose:
                print(f"Sample:\n{play}")
            stream.write(play)
            sleep(0.02)
        stream.close()
    if out_wav != "":
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
