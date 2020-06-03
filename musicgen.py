from random import randint as rint
# ----------
# Config:
# ----------
# Whether to output sound (Set to False to reduce wait time for out_wav file, if applicable):
out_sound = True


# Path to sf2 file (Leave the string empty to disable, plays with sine wave if disabled):
sf2 = ""
# sf2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"


# Audio driver to use (Leave the stringe empty for system default, Linux users may need to specify alsa):
audio_driver = ""
# audio_driver = "alsa"


# Path to output / name of wav file (Leave the string empty to disable)
# Ensure any folders already exist but the wave file does not!:
out_wav = ""
# out_wav = "out7.wav"


# Whether to output the actual keys or just the numerical notes:
out_keys = False


# Whether to output lots of details or just the notes (True or False):
verbose = False


# Set to the desired number of phrases:
stop_point = 15


# Set to the desired pitch multiplier (greater value = greater pitch; lowest is 1)
# CURRENTLY ANYTHING GREATER THAN ONE(1) IS INSANELY HIGH PITCHED!!!:
pitch_multiplier = 1


# Set to the desired playback BPM:
bpm = 120


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
bpm = int(bpm)
# ----------


# ----------
# Main mechanism:
# -----
# Define lots of functions:
def run_lnotes(code):
    def lnotes_pos():
        return notes[index][index1][index2][index3]
    for index, lrep_code in enumerate(notes):
        for index1, lrep_code1 in enumerate(lrep_code):
            for index2, lrep_code2 in enumerate(lrep_code1):
                for index3, lrep_code3 in enumerate(lrep_code2):
                    exec(code)


def beats_per_bar():
    return sig[0]


def pick_scale(scale_base):
    if rint(1, 2) == 1:
        return first_note()[0] + scale[scale_base]
    else:
        return first_note()[0] - scale[scale_base]


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


def app_beat():
    if int(beats_per_bar()/last_note()[0]) < 1 or len(notes) <= 1:
        return rint(1, 2)
    else:
        if int(beats_per_bar()/last_note()[0]) + sum([b[1] for b in last_subbar()]) > beats_per_bar():
            return beats_per_bar() - sum([b[1] for b in last_subbar()])
        else:
            return int(beats_per_bar()/last_note()[0])


def mk_compose():
    # Append a note from the scale of the first note:
    last_subbar().append([pick_scale(rint(1, 7)), app_beat()])
    # Append a rest if there aren't too many:
    if last_subbar().count(-1) < len(last_subbar())/1.5 and rint(1, 2) == 1:
        last_subbar().append([-1, app_beat()])


def mk_compose_ud(up_down):
    # Same as mk_compose but for the high or low end of the scale only:
    if up_down == 1:
        last_subbar().append([pick_scale(rint(4, 7)), app_beat()])
    else:
        last_subbar().append([pick_scale(rint(1, 4)), app_beat()])
    if last_subbar().count(-1) < len(last_subbar())/1.5 and rint(1, 2) == 1:
        last_subbar().append([-1, app_beat()])


def compose_phrase():
    while sum([b[1] for b in last_subbar()]) < beats_per_bar()/2:
        mk_compose()
    up_down = rint(1, 2)
    while sum([b[1] for b in last_subbar()]) < beats_per_bar():
        mk_compose_ud(up_down)
    for lvary in range(0, rint(0, 6)):
        last_bar().append(last_subbar()[0:int(len(last_subbar())/2)])
        up_down = rint(1, 2)
        while sum([b[1] for b in last_subbar()]) < sig[0]:
            mk_compose_ud(up_down)


# -----
# Actually run now:
sig = [rint(9, 18), 2**rint(1, 4)]
notes = [[[[[rint(24, 36)]]]]]
last_note().append(int(beats_per_bar()/last_note()[0]))
bpm = first_note()[0] * 7
while len(notes) < stop_point:
    # print(notes)
    if rint(1, 2) == 1:
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
        scale = {
            1: 2,
            2: 3,
            3: 5,
            4: 7,
            5: 8,
            6: 10,
            7: 12
        }
    compose_phrase()
    if rint(1, 2) == 1:
        notes.append([[[[first_note()[0], app_beat()]]]])
    else:
        notes.append([[[[first_last_note()[0], app_beat()]]]])


if fix_pitch:
    run_lnotes(
        """
if lnotes_pos()[0] != -1:
    while lnotes_pos()[0] < 24:
        lnotes_pos()[0] += 12
    while lnotes_pos()[0] > 48:
        lnotes_pos()[0] -= 12
        """
        )


if pitch_multiplier > 1:
    run_lnotes(
        """
if lnotes_pos()[0] != -1:
    lnotes_pos()[0] += int(12*(pitch_multiplier-1))
        """
    )
print("----------")
print(f"Key signature: {sig[0]}/{sig[1]}")
print(f"Final notes (numerical): {notes}")
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
    for lkey_out in key_out:
        print(lkey_out)
    print("----------")
# ----------


# ----------
# Output result if enabled:
if out_sound or out_wav != "":
    # If you see a warning about numpy not being used,
    # That's just because it's in a string to be passed to a function :)
    import numpy as np
    if out_wav:
        import wave
    import pyaudio
    sr = 44100
    samples = []
    if sf2 != "":
        from mingus.midi import fluidsynth
        from time import sleep
        if audio_driver != "":
            fluidsynth.init(sf2, audio_driver)
        else:
            fluidsynth.init(sf2)
        run_lnotes(
            """
if lrep_code3[0] == -1:
    sleep(lrep_code3[1]*(60/bpm))
else:
    fluidsynth.play_Note(lrep_code3[0]-1, 0, volume*100)
            """
        )
    if out_wav != "" or sf2 == "":
        run_lnotes(
            """
if lrep_code3[0] == -1:
    freq = 0
else:
    freq = 27.5*(2**(lrep_code3[0]/12))
samples.append(
    np.sin(2*np.pi*np.arange(sr*lrep_code3[1]*(60/bpm))*freq/sr)
    .astype(np.float32)*volume)
        """
        )
    if sf2 == "":
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
                stream.close()
                sleep(0.02)
        p.terminate()
    if out_wav != "":
        wf = wave.open(out_wav, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
        wf.setframerate(sr)
        wf.writeframes(b''.join(samples))
        wf.close()
print("Done!")
print(f"I wrote {len(notes)} phrases,")
print(f"{sum([sum([len(b) for b in p]) for p in notes])} bars,")
print(f"and {sum([sum([len([sum([len(n) for n in b]) for p in notes]) for b in p]) for p in notes])} notes!")
print("Exiting...")
# ----------
