#
# tet.py : Twelve-tone Equal Temperment (TET) 
# See tet.html for module documentation.

import math
#Works
def hertz_to_midi(hertz):
    if (hertz < 0):
        raise ValueError
    midi = round(69 + math.log((hertz/440.0), 2) * 12)
    check_midi(midi)
    return midi

#Works
def midi_to_hertz(midi):
    check_midi(midi)
    hertz = 440.0 * 2 ** ((midi-69)/12)
    return hertz

#Works
def midi_to_pc(midi):
    check_midi(midi)
    pc = midi % 12
    return pc

#Works
def pitch_to_midi(pitch):
    pc_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    pc = ''
    octave = ''
    accidental = ''
    note_name = ''
    for char in pitch:
        if (char == '0' or char == '1' or char == '2' or char == '3' or char == '4' or
        char == '5' or char == '6' or char == '7' or char == '8' or char == '9'):
            octave += char
        elif (char == 'b' or char == 'f' or char == '#' or char == 's'):
            accidental += char
        else:
            note_name += char
    #pitch is seperated into name, accidental, and octave
    if (not pitch.endswith(octave)):
        raise ValueError
    #identify pitch class
    for item in pc_list:
        if (note_name == item):
            pc = item
    #pitch class identified

    midi = pc_list.index(pc)
    if (octave == '0' or octave == '00'):
        midi = midi + 12 * int(octave)
    else:
        midi = midi + 12 * (int(octave) + 1)
    #Adjusting midi by accidental
    if (accidental == 'b' or accidental == 'f'):
        midi = midi - 1
    elif (accidental == 'bb' or accidental == 'ff'):
        midi = midi - 2
    elif (accidental == '#' or accidental == 's'):
        midi = midi + 1
    elif (accidental == '##' or accidental == 'ss'):
        midi = midi + 2
    elif (accidental != ""):
        raise ValueError
    check_midi(midi)
    return midi
    
#Works
def midi_to_pitch(midi, accidental=None):
    pc_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
    if (accidental != 'b' and accidental != 'bb' and accidental != '#' and accidental != '##' and
    accidental != 'f' and accidental != 'ff' and accidental != 's' and accidental != 'ss' and accidental != None):
        raise ValueError
    if (accidental == 'b' or accidental == 'f'):
        midi = midi + 1
    elif (accidental == 'bb' or accidental == 'ff'):
        midi = midi + 2
    elif (accidental == '#' or accidental == 's'):
        midi = midi - 1
    elif (accidental == '##' or accidental == 'ss'):
        midi = midi - 2
    pc_index = midi_to_pc(midi)
    if (accidental != None):
        pitch = pc_list[pc_index] + accidental
    else:
        pitch = pc_list[pc_index]
    octave = int((midi / 12) - 1)
    pitch += str(octave)
    if (octave == 0):
        pitch += '0'
    #Check if pitch is valid
    check_pitch(pitch, accidental)
    return pitch

#Relies on above functions
#Works
def hertz_to_pitch(hertz):
    midi = hertz_to_midi(hertz)
    return midi_to_pitch(midi)

#Relies on above functions
#Works
def pitch_to_hertz(pitch):
    check_pitch(pitch, getAccidental(pitch))
    midi = pitch_to_midi(pitch)
    return midi_to_hertz(midi)

def getAccidental(pitch):
    output = ''
    for c in pitch:
        if (c == 'b' or c == 'f' or c == 's' or c == '#'):
            output += c
    return output


def check_midi(midi):
    if (midi < 0 or midi > 127):
        raise ValueError
    if (not isinstance(midi, int)):
        raise ValueError

def check_pitch(pitch, accidental):
    pitch_letters = 0
    pitch_accidentals = 0
    pitch_octaves = 0
    for c in pitch:
        if (c.isupper()):
            pitch_letters += 1
        elif (c.isdigit()):
            pitch_octaves += 1
        elif (c == 'b' or c == 'f' or c == '#' or c == 's'):
            pitch_accidentals += 1
    if(pitch.endswith("00")):
        pitch_octaves -= 1
    if (accidental != None and (pitch_letters > 1 or pitch_octaves > 1 or pitch_accidentals > 2 or len(accidental) < pitch_accidentals)):
        raise ValueError

if __name__ == '__main__':
    print("Testing...")
    print(midi_to_pitch(48, '##'))
    print("Done!")