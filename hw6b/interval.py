###############################################################################
from .pitch import Pitch
#Span values
_unison, _second, _third, _fourth, _fifth, _sixth, _seventh, _octave = (i for i in range(8))
_span_names = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh", "octave"]
#Quality values
_dim5, _dim4, _dim3, _dim2, _dim, _minor, _perfect, _major, _aug, _aug2, _aug3, _aug4, _aug5 = (i for i in range(13))
_unsafe_qual_names = ["ooooo", "oooo", "ooo", "oo", "o", "m", "P", "M", "+", "++", "+++", "++++", "+++++"]
_safe_qual_names = ["ddddd", "dddd", "ddd", "dd", "d", "m", "P", "M", "A", "AA", "AAA", "AAAA", "AAAAA"]
class Interval:
    def __init__(self, arg, other=None):
        if(isinstance(arg, str)):
            self._init_from_string(arg)
        elif(isinstance(arg, list)):
            self._init_from_list(arg[0],arg[1],arg[2],arg[3])
        elif(isinstance(arg, Pitch) and isinstance(other, Pitch)):
            self._init_from_pitches(arg, other)
        else:
            raise TypeError


    def _init_from_list(self, span, qual, xoct, sign):
        #Check if values in range
        if(span < 0 or span > 7):
            raise ValueError
        if(qual < 0 or qual > 12):
            raise ValueError
        if(xoct < 0 or xoct > 10):
            raise ValueError
        if(sign != -1 and sign != 1):
            raise ValueError
        #Edge cases
        if(xoct > 1 and span == 0):
            span = 7
            xoct = xoct - 1
        #Less than Perfect Unison
        if((span+7*xoct)==_unison and qual < _perfect):
            raise ValueError
        #Less than dim 2nd
        if((span+7*xoct)==_second and qual < _dim):
            raise ValueError
        #Less than triple dim 3rd
        if((span+7*xoct)==_third and qual < _dim3):
            raise ValueError
        #Only 5th can be quintuply dim
        if(span!=_fifth and qual==_dim5):
            raise ValueError
        #Only 4th can be quintuply aug
        if(span!=_fourth and qual==_aug5):
            raise ValueError
        #Last legal interval: 10 octave perfect 5th
        if(span==_fifth and xoct==10 and qual>_perfect):
            raise ValueError
        if(span==_sixth and xoct==10 and qual>_dim):
            raise ValueError
        if(span==_unison and xoct==1):
            span = _octave
            xoct = 0
        if((span==_unison or span==_fourth or span==_fifth or span==_octave) and (qual==_major or qual==_minor)):
            raise ValueError
        if((span==_second or span==_third or span==_sixth or span==_seventh) and qual==_perfect):
            raise ValueError
        self.span=span
        self.qual=qual
        self.xoct=xoct
        self.sign=sign
    
    
    def _init_from_string(self, name):
        if(len(name) < 2):
            raise ValueError
        span, qual = "", ""
        sign = 1
        for char in name:
            if(char.isnumeric()):
                span += char
            elif(char == '-'):
                sign = -1
            else:
                qual += char
        if(sign == -1 and name[0] != '-'):
            raise ValueError
        input_span = (int(span)-1) % 7
        if(int(span)-1 == -1):
            input_span = 0
        if((int(span)-1)%7 == 0 and int(span) > 7):
            input_span = _octave
        xoct = 0
        if(int(span) > 8):
            xoct = int((int(span)/7))
        input_qual = -1
        if(qual == "P"):
            input_qual = _perfect
        elif(qual == "M"):
            input_qual = _major
        elif(qual == "m"):
            input_qual = _minor
        elif(qual == "o" or qual == "d"):
            input_qual = _dim
        elif(qual == "oo" or qual == "dd"):
            input_qual = _dim2
        elif(qual == "ooo" or qual == "ddd"):
            input_qual = _dim3
        elif(qual == "oooo" or qual == "dddd"):
            input_qual = _dim4
        elif(qual == "ooooo" or qual == "ddddd"):
            input_qual = _dim5
        elif(qual == "+" or qual == "A"):
            input_qual = _aug
        elif(qual == "++" or qual == "AA"):
            input_qual = _aug2
        elif(qual == "+++" or qual == "AAA"):
            input_qual = _aug3
        elif(qual == "++++" or qual == "AAAA"):
            input_qual = _aug4
        elif(qual == "+++++" or qual == "AAAAA"):
            input_qual = _aug5
        self._init_from_list(input_span, input_qual, xoct, sign)          


    def _init_from_pitches(self, pitch1, pitch2):
        #Pitch Attributes:
        #letter C-B (0-6)
        #accidental bb-## (0-4)
        #octave 00-9 (0-10)
        sign=-1
        if(pitch1 <= pitch2):
            sign = 1
        span = ((pitch2.letter - pitch1.letter) * sign) % _octave
        semitones = (pitch2.keynum() - pitch1.keynum()) * sign
        # print(f"Semi: {semitones}\n")
        if(semitones>=12 and span == 0):
            span = _octave
        xoct = 0
        if(semitones > 12):
            xoct = (int)(semitones/12)
            if(semitones/12 < 1):
                xoct = 0
            if(span == _octave):
                xoct = xoct-1
        semitones = semitones%12
        # print(f"Semi: {semitones}\n")
        qual=-1
        if(span==_unison):
            if(semitones == 0):
                qual=_perfect
            if(semitones == 1):
                qual=_aug
            if(semitones == 2):
                qual=_aug2
            if(semitones == 3):
                qual=_aug3
            if(semitones == 4):
                qual=_aug4
        if(span==_second):
            if(semitones == 0):
                qual=_dim
            if(semitones == 1):
                qual=_minor
            if(semitones == 2):
                qual=_major
            if(semitones == 3):
                qual=_aug
            if(semitones == 4):
                qual=_aug2
            if(semitones == 5):
                qual=_aug3
            if(semitones == 6):
                qual=_aug4
        if(span==_third):
            if(semitones==0):
                qual=_dim3
            if(semitones==1):
                qual=_dim2
            if(semitones==2):
                qual=_dim
            if(semitones==3):
                qual=_minor
            if(semitones == 4):
                qual=_major
            if(semitones==5):
                qual=_aug
            if(semitones==6):
                qual=_aug2
            if(semitones==7):
                qual=_aug3
            if(semitones==8):
                qual=_aug4
        if(span==_fourth):
            if(semitones==1):
                qual=_dim4
            if(semitones==2):
                qual=_dim3
            if(semitones==3):
                qual=_dim2
            if(semitones==4):
                qual=_dim
            if(semitones==5):
                qual=_perfect
            if(semitones==6):
                qual=_aug
            if(semitones==7):
                qual=_aug2
            if(semitones==8):
                qual=_aug3
            if(semitones==9):
                qual=_aug4
            if(semitones==10):
                qual=_aug5
        if(span==_fifth):
            if(semitones==2):
                qual=_dim5
            if(semitones==3):
                qual=_dim4
            if(semitones==4):
                qual=_dim3
            if(semitones==5):
                qual=_dim2
            if(semitones==6):
                qual=_dim
            if(semitones==7):
                qual=_perfect
            if(semitones==8):
                qual=_aug
            if(semitones==9):
                qual=_aug2
            if(semitones==10):
                qual=_aug3
            if(semitones==11):
                qual=_aug4
        if(span==_sixth):
            if(semitones==4):
                qual=_dim4
            if(semitones==5):
                qual=_dim3
            if(semitones==6):
                qual=_dim2
            if(semitones==7):
                qual=_dim
            if(semitones==8):
                qual=_minor
            if(semitones==9):
                qual=_major
            if(semitones==10):
                qual=_aug
            if(semitones==11):
                qual=_aug2
            if(semitones==0):
                qual=_aug3
            if(semitones==1):
                qual=_aug4
        if(span==_seventh):
            if(semitones==6):
                qual=_dim4
            if(semitones==7):
                qual=_dim3
            if(semitones==8):
                qual=_dim2
            if(semitones==9):
                qual=_dim
            if(semitones==10):
                qual=_minor
            if(semitones==11):
                qual=_major
            if(semitones==0):
                qual=_aug
            if(semitones==1):
                qual=_aug2
            if(semitones==2):
                qual=_aug3
            if(semitones==3):
                qual=_aug4
        if(span==_octave):
            if(semitones==8):
                qual=_dim4
            if(semitones==9):
                qual=_dim3
            if(semitones==10):
                qual=_dim2
            if(semitones==11):
                qual=_dim
            if(semitones==0):
                qual = _perfect
            if(semitones==1):
                qual=_aug
            if(semitones==2):
                qual=_aug2
            if(semitones==3):
                qual=_aug3
            if(semitones==4):
                qual=_aug4
        print(f"Span: {span} \nQual: {qual} \nXoct: {xoct} \nSign: {sign}")
        self._init_from_list(span, qual, xoct, sign)
    

    def __str__(self):
        if(self.sign == -1):
            return f'<Interval: -{_unsafe_qual_names[self.qual]}{(self.span+1)+(7*self.xoct)} [{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'
        return f'<Interval: {_unsafe_qual_names[self.qual]}{(self.span+1)+(7*self.xoct)} [{self.span}, {self.qual}, {self.xoct}, {self.sign}] {hex(id(self))}>'


    def __repr__(self):
        return f'Interval(\"{self.string()}\")'


    def __lt__(self, other):
        if(isinstance(other, Interval)):
            return self.pos() < other.pos()
        else:
            raise TypeError


    def __le__(self, other):
        if(isinstance(other, Interval)):
            return self.pos() <= other.pos()
        else:
            raise TypeError


    def __eq__(self, other):
        if(isinstance(other, Interval)):
            return self.pos() == other.pos()
        else:
            raise TypeError


    def __ne__(self, other):
        if(isinstance(other, Interval)):
            return self.pos() != other.pos()
        else:
            raise TypeError


    def __ge__(self, other):
        if(isinstance(other, Interval)):
            return self.pos() >= other.pos()
        else:
            raise TypeError


    def __gt__(self, other):
        if(isinstance(other, Interval)):
            return self.pos() > other.pos()
        else:
            raise TypeError

  
    def pos(self):
        return (((self.span + (self.xoct*7)) + 1) << 8) + self.qual


    def string(self):
        total_string = ""
        if(self.sign == -1):
            total_string += "-"
        total_string += _unsafe_qual_names[self.qual]
        if(self.xoct ==0):
            total_string += str(self.span+1)
        else:
            total_string += str(self.span+1+ (7*self.xoct))
        return total_string


    def full_name(self, *, sign=False):
        quality = self.quality_name()
        if(sign):
            return f"descending {quality} {self.span_name()}"
        return f"{quality} {self.span_name()}"


    def span_name(self):
        return _span_names[self.span]


    def quality_name(self):
        qual = _unsafe_qual_names[self.qual]
        if(qual == 'ooooo'):
            return 'quintuply-diminished'
        if(qual == 'oooo'):
            return 'quadruply-diminished'
        if(qual == 'ooo'):
            return 'triply-diminished'
        if(qual == 'oo'):
            return 'doubly-diminished'
        if(qual == 'o'):
            return 'diminished'
        if(qual == 'm'):
            return 'minor'
        if(qual == 'M'):
            return 'major'
        if(qual == 'P'):
            return 'perfect'
        if(qual == '+++++'):
            return 'quintuply-augmented'
        if(qual == '++++'):
            return 'quadruply-augmented'
        if(qual == '+++'):
            return 'triply-augmented'
        if(qual == '++'):
            return 'doubly-augmented'
        if(qual == '+'):
            return 'augmented'

    
    def matches(self, other):
        if(not isinstance(other, Interval)):
            raise TypeError
        if(self.span != other.span):
            return False
        if(self.qual != other.qual):
            return False
        if(self.sign != other.sign):
            return False
        return True


    def lines_and_spaces(self):
        return self.span+1


    def _to_iq(self, name):
        if(name == "o" or "d"):
            return _dim
        if(name == "oo" or "dd"):
            return _dim2
        if(name == "ooo" or "ddd"):
            return _dim3
        if(name == "oooo" or "dddd"):
            return _dim4
        if(name == "ooooo" or "ddddd"):
            return _dim5
        if(name == "A" or "+"):
            return _aug
        if(name == "AA" or "++"):
            return _aug2
        if(name == "AAA" or "+++"):
            return _aug3
        if(name == "AAAA" or "++++"):
            return _aug4
        if(name == "AAAAA" or "+++++"):
            return _aug5
        if(name == "P"):
            return _perfect
        if(name == "M"):
            return _major
        if(name == "m"):
            return _minor
        

    def to_list(self):
        return [self.span, self.qual, self.xoct, self.sign]


    def is_unison(self, qual=None):
        if(self.span != _unison):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            # print(quality_number)
            if(quality_number == _major or quality_number == _minor or quality_number==_aug5 or quality_number==_dim5):
                return False
        return True


    def is_second(self, qual=None):
        if(self.span != _second):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _perfect or quality_number==_aug5 or quality_number==_dim5):
                return False
        return True
    

    def is_third(self, qual=None):
        if(self.span != _third):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _perfect or quality_number==_aug5 or quality_number==_dim5):
                return False
        return True


    def is_fourth(self, qual=None):
        if(self.span != _fourth):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _major or quality_number==_minor or quality_number==_dim5):
                return False
        return True


    def is_fifth(self, qual=None):
        if(self.span != _fifth):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _major or quality_number==_minor or quality_number==_aug5):
                return False
        return True


    def is_sixth(self, qual=None):
        if(self.span != _sixth):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _perfect or quality_number==_aug5 or quality_number==_dim5):
                return False
        return True


    def is_seventh(self, qual=None):
        if(self.span != _seventh):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _perfect or quality_number==_aug5 or quality_number==_dim5):
                return False
        return True

    
    def is_octave(self, qual=None):
        if(self.span != _octave):
            return False
        if(qual != None):
            if(self.is_augmented()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(self.is_diminished()):
                if(_unsafe_qual_names.__contains__(qual)):
                    if(_unsafe_qual_names.index(qual) != self.qual):
                        return False
                elif(_safe_qual_names.__contains__(qual)):
                    if(_safe_qual_names.index(qual) != self.qual):
                        return False
            elif(_unsafe_qual_names.index(qual) != self.qual):
                return False
            quality_number = self._to_iq(qual)
            if(quality_number == _major or quality_number==_minor or quality_number==_aug5 or quality_number==_dim5):
                return False
        return True


    def is_diminished(self):
        quality = self.qual
        if(quality == _dim):
            return 1
        if(quality == _dim2):
            return 2
        if(quality == _dim3):
            return 3
        if(quality == _dim4):
            return 4
        if(quality == _dim5):
            return 5
        return False
    

    def is_minor(self):
        return self.qual == _minor

    
    def is_perfect(self):
        return self.qual == _perfect

    
    def is_major(self):
        return self.qual == _major

    
    def is_augmented(self):
        quality = self.qual
        print(quality)
        if(quality == _aug):
            return 1
        if(quality == _aug2):
            return 2
        if(quality == _aug3):
            return 3
        if(quality == _aug4):
            return 4
        if(quality == _aug5):
            return 5
        return False
    

    def is_perfect_type(self):
        return self.span == _unison or self.span == _fourth or self.span == _fifth or self.span == _octave

    
    def is_imperfect_type(self):
        return not self.is_perfect_type()

        
    def is_simple(self):
        return self.xoct==0

        
    def is_compound(self):
        return self.xoct>0

    
    def is_ascending(self):
        return self.sign==1

    
    def is_descending(self):
        return self.sign==-1

    
    def is_consonant(self):
        if(self.span == _unison or self.span == _fourth or self.span == _fifth or self.span == _octave):
            if(self.qual != _perfect):
                return False
        if(self.span == _third or self.span == _sixth):
            if(self.qual != _major and self.qual != _minor):
                return False
        if(self.span == _second or self.span == _seventh):
            return False
        return True

                   
    def is_dissonant(self):
        return not self.is_consonant()


    def complemented(self):
        inverted_span = 7 - self.span
        inverted_qual = _aug5 - self.qual
        return Interval([inverted_span, inverted_qual, 0, 1])

    
    def semitones(self):
        output = 0
        if(self.is_unison()):
            output = 0
        if(self.is_second()):
            output = 2
        if(self.is_third()):
            output = 4
        if(self.is_fourth()):
            output = 5
        if(self.is_fifth()):
            output = 7
        if(self.is_sixth()):
            output = 9
        if(self.is_seventh()):
            output = 11
        if(self.is_octave()):
            output = 12
        if(self.is_minor()):
            output = output-1
        if(self.is_augmented() == 1):
            output = output+1
        if(self.is_augmented() == 2):
            output = output+2
        if(self.is_augmented() == 3):
            output = output+3
        if(self.is_augmented() == 4):
            output = output+4
        if(self.is_augmented() == 5):
            output = output+5
        if(self.is_diminished() == 1):
            if(self.is_perfect_type()):
                output = output-1
            else:
                output = output-2
        if(self.is_diminished() == 2):
            if(self.is_perfect_type()):
                output = output-2
            else:
                output = output-3
        if(self.is_diminished() == 3):
            if(self.is_perfect_type()):
                output = output-3
            else:
                output = output-4
        if(self.is_diminished() == 4):
            if(self.is_perfect_type()):
                output = output-4
            else:
                output = output-5
        if(self.is_diminished() == 5):
            if(self.is_perfect_type()):
                output = output-5
            else:
                output = output-6
        if(self.is_descending()):
            return -(output+12*self.xoct)
        return output+12*self.xoct


    def add(self, other):
        if(not isinstance(other, Interval)):
            raise TypeError
        if(self.is_descending() or other.is_descending()):
            raise NotImplementedError
        input_span = -1
        input_qual = -1
        if(other.span == _third):
            input_span = 2 + self.span
        if(input_span == _fifth):
            if(self.qual == _major and other.qual == _minor):
                input_qual = _perfect
            elif(self.qual == _minor and other.qual == _minor):
                input_qual = _dim
            elif(self.qual == _major and other.qual == _major):
                input_qual = _aug
        if(input_span == _seventh):
            if(self.qual == _perfect and other.qual == _minor):
                input_qual = _minor
            elif(self.qual == _dim and other.qual == _minor):
                input_qual = _dim
        return Interval([input_span, input_qual, 0, 1])


    def transpose(self, p):
        if(isinstance(p, Pitch)):
            midi = p.keynum() + self.semitones()
            return p.from_keynum(midi)
        elif(isinstance(p, str)):
            pass
        else:
            raise TypeError

if __name__ == '__main__':
    # Add your testing code here!
    print("Testing...")
    print(Interval(Pitch('Eb4'), Pitch('D##5')))
    print("Done")
    pass

