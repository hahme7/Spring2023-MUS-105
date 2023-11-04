###############################################################################
"""
A class that implements musical pitches.

The Pitch class represent equal tempered pitches and returns information
in hertz, keynum, pitch class, Pnum  and pitch name formats.  Pitches
can be compared using standard math relations and maintain proper spelling
when complemented or transposed by an Interval.
"""

from enum import IntEnum
from math import pow
from collections import namedtuple

# Create the namedtuple super class for Pitch with three attributes:
# letter, accidental, and octave.  See your ratio.py file for an example.
PitchBase = namedtuple('PitchBase', ['letter', 'accidental', 'octave'])


class Pitch (PitchBase):


    # Create the pnum class here, see documentation in pitch.html
    # C = 0 
    # B = 6
    # ff = 0
    # ss = 4
    list_of_tuples = [('Cff', 0b00000000), ('Cf', 0b00000001), ('C', 0b00000010), ('Cs', 0b00000011), ('Css', 0b00000100),
                      ('Dff', 0b00010000), ('Df', 0b00011001), ('D', 0b00010010), ('Ds', 0b00010011), ('Dss', 0b00010100),
                      ('Eff', 0b00100000), ('Ef', 0b00101001), ('E', 0b00100010), ('Es', 0b00100011), ('Ess', 0b00100100),
                      ('Fff', 0b00110000), ('Ff', 0b00111001), ('F', 0b00110010), ('Fs', 0b00110011), ('Fss', 0b00110100),
                      ('Gff', 0b01000000), ('Gf', 0b01001001), ('G', 0b01000010), ('Gs', 0b01000011), ('Gss', 0b01000100),
                      ('Aff', 0b01010000), ('Af', 0b01011001), ('A', 0b01010010), ('As', 0b01010011), ('Ass', 0b01010100),
                      ('Bff', 0b01100000), ('Bf', 0b01101001), ('B', 0b01100010), ('Bs', 0b01100011), ('Bss', 0b01100100)]
    pnums = IntEnum('Pnum', list_of_tuples)
    

    def __new__(cls, arg=None):
        if(isinstance(arg, str)):
            return cls._string_to_pitch(arg)
        if(isinstance(arg, list) and len(arg) == 3):
            return cls._values_to_pitch(arg[0], arg[1], arg[2])
        if(arg == None):
            return super(Pitch, cls).__new__(cls, None, None, None)
        raise TypeError


    @classmethod
    def _string_to_pitch(cls, arg):
        letter, accidental, octave = "","",""
        pitch_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        unsafe_accidentals = ['bb', 'b', '', '#', '##']
        safe_accidentals = ['ff', 'f', 'n', 's', 'ss']
        octaves = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if arg[0].islower():
            arg = arg.capitalize()
        for i in range(len(arg)):
            c = arg[i]
            if(i == 0):
                letter = c
                continue
            if((i == 1 or i == 2) and (c in unsafe_accidentals or c in safe_accidentals)):
                accidental += c
                continue
            if((i == 1 or i == 2 or i == 3 or i == 4) and c.isnumeric()):
                octave += c
                if(i+1 < len(arg)):
                    if(arg[i+1] == '0'):
                        octave += '0'
                break
            raise TypeError
        if(arg[len(arg)-1] != octave[0]):
            raise TypeError
        letter = pitch_letters.index(letter)
        if accidental in unsafe_accidentals:
            accidental = unsafe_accidentals.index(accidental)
        else:
            accidental = safe_accidentals.index(accidental)
        octave = octaves.index(octave)        
        return cls._values_to_pitch(letter, accidental, octave)


    @classmethod
    def _values_to_pitch(cls, let, acc, ova):
        pitch_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        unsafe_accidentals = ['bb', 'b', '', '#', '##']
        octaves = ['00', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if(let < 0 or acc < 0 or ova < 0):
            raise ValueError
        if(let > 6 or acc > 4 or ova > 10):
            raise ValueError
        if(let == 0 and acc < 2 and ova == 0):
            raise ValueError
        if((ova == 10 and let == 4) and acc > 2):
            raise ValueError
        if((ova == 10 and let == 5) and acc != 0):
            raise ValueError
        return super(Pitch, cls).__new__(cls, pitch_letters[let], unsafe_accidentals[acc], octaves[ova])
        


    def __str__(self):
        # It is important that you implement the __str__ method precisely.
        # In particular, for __str__ you want to see '<', '>', '0x' in 
        # your output string.  The format of your output strings from your
        # version of this function must look EXACTLY the same as in the two
        # examples below.
        # 
        #     >>> str(Pitch("C#6"))
        #     '<Pitch: C#6 0x7fdb17e2e950>'
        #     >>> str(Pitch())
        #     '<Pitch: empty 0x7fdb1898fa70>'
        if self.is_empty():
            return f"'<Pitch: empty 0x{id(self)}>'"
        return f"<Pitch: {self.letter}{self.accidental}{self.octave} {hex(id(self))}>"


    def __repr__(self):
        # Note: It is the __repr__ (not the __str__) function that the autograder
        # uses to compare results. So it is very important that you implement this
        # method precisely. In particular, for __repr__ you want to see double
        # quotes inside single quotes and NOT the other way around. The format of
        # your output strings from your version of this function must look 
        # EXACTLY the same as in the two examples below.
        #
        #     >>> str(Pitch("C#6"))
        #     '<Pitch: C#6 0x7fdb17e2e950>'
        #     >>> repr(Pitch("Bbb3"))
        #     'Pitch("Bbb3")'
        return f"'Pitch(\"{self.letter}{self.accidental}{self.octave}\")'"


    def __lt__(self, other):
       if(not isinstance(other, Pitch)):
            raise TypeError
       return self.pos() < other.pos()


    def __le__(self, other):
        if(self.__eq__(other) or self.__lt__(other)):
            return True
        return False


    def __eq__(self, other):
        if(not isinstance(other, Pitch)):
            raise TypeError
        return self.pos() == other.pos()


    def __ne__(self, other):
        if(not isinstance(other, Pitch)):
            raise TypeError
        return self.pos() != other.pos()


    def __ge__(self, other):
        if(self.__eq__(other) or self.__gt__(other)):
            return True
        return False


    def __gt__(self, other):
        if(not isinstance(other, Pitch)):
            raise TypeError
        return self.pos() > other.pos()


    def pos(self):
        pitch_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
        unsafe_accidentals = ['bb', 'b', '', '#', '##']
        safe_accidentals = ['ff', 'f', 'n', 's', 'ss']
        ova = int(self.octave)
        let = pitch_letters.index(self.letter)
        if(self.accidental == 'bb' or self.accidental == 'b' or self.accidental == '#' or self.accidental == '##' or self.accidental == ''):
            acc = unsafe_accidentals.index(self.accidental)
        else:
            acc = safe_accidentals.index(self.accidental)
        return (ova<<8) + (let<<4) + acc


    def is_empty(self):
        return self.letter == None


    def string(self):
        return f'{self.letter}{self.accidental}{self.octave}'


    def keynum(self):
        midi = self.pc()
        if (self.octave == '0' or self.octave == '00'):
            midi = midi + 12 * int(self.octave)
        else:
            midi = midi + 12 * (int(self.octave) + 1)
        return midi


    def pnum(self):
        if (self.accidental == '#'):
            temp = self.letter + 's'
        elif (self.accidental =='##'):
            temp = self.letter + 'ss'
        elif(self.accidental=='b'):
            temp = self.letter + 'f'
        elif(self.accidental=='bb'):
            temp = self.letter + 'ff'
        else:
            temp = self.letter + self.accidental 
        return self.pnums[temp]

    
    def pc(self):
        pc_list = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        output = pc_list.index(self.letter)
        if(self.accidental == 'bb' or self.accidental == 'ff'):
            return (output-2) % 12
        if(self.accidental == 'b' or self.accidental == 'f'):
            return (output-1)%12
        if(self.accidental == '#' or self.accidental == 's'):
            return (output+1)%12
        if(self.accidental == '##' or self.accidental == 'ss'):
            return (output+2)%12
        return output

    
    def hertz(self):
        midi = self.keynum()
        hertz = 440.0 * 2 ** ((midi-69)/12)
        return hertz


    @classmethod
    def from_keynum(cls, keynum, acci=None):
        arr = ['C', 'Cs', 'D', 'Ef', 'E', 'F', 'Fs', 'G', 'Af', 'A', 'Bf', 'B']
        if(acci == 'ff' or acci == 'bb'):
            keynum += 2
        elif(acci == 'f' or acci == 'b'):
            keynum += 1
        elif(acci == 's' or acci == '#'):
            keynum -= 1
        elif(acci == 'ss' or acci == '##'):
            keynum -= 2
        if(keynum < 0 or keynum > 127):
            raise ValueError
        letter = arr[keynum%12]
        if(len(letter) == 2 and acci != None): #Has accidental already
            raise ValueError
        if(acci != None):
            pitch = letter + acci
        else:
            pitch = letter
        octave = str(int((keynum/12)-1))
        pitch += octave
        return Pitch(pitch)




if __name__ == '__main__':
    print("Testing: ")
    
    print(repr(Pitch('Cs5')))
    print("Done")

