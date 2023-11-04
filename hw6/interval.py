###############################################################################

# from .pitch import Pitch
#Span values
_unison, _second, _third, _fourth, _fifth, _sixth, _seventh, _octave = (i for i in range(8))
_span_names = ["unison", "second", "third", "fourth", "fifth", "sixth", "seventh", "octave"]
#Quality values
_dim5, _dim4, _dim3, _dim2, _dim, _minor, _perfect, _major, _aug, _aug2, _aug3, _aug4, _aug5 = (i for i in range(13))
_unsafe_qual_names = ["ooooo", "oooo", "ooo", "oo", "o", "m", "P", "M", "+", "++", "+++", "++++", "+++++"]
_safe_qual_names = ["ddddd", "dddd", "ddd", "dd", "d", "m", "P", "M", "a", "aa", "aaa", "aaaa", "aaaaa"]
class Interval:
    
    def __init__(self, arg, other=None):
        if(isinstance(arg, str)):
            self._init_from_string(arg)
        elif(isinstance(arg, list)):
            self._init_from_list(arg[0],arg[1],arg[2],arg[3])
        # elif(isinstance(arg, Pitch) and isinstance(other, Pitch)):
            # self._init_from_pitches(arg, other)
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
        if(sign != -1 or sign != 1):
            raise ValueError
        #Edge cases
        #Less than Perfect Unison
        if(span==_unison and qual < _perfect):
            raise ValueError
        #Less than dim 2nd
        if(span==_second and qual < _dim):
            raise ValueError
        #Less than triple dim 3rd
        if(span==_third and qual < _dim3):
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
        self.span=span
        self.qual=qual
        self.xoct=xoct
        self.sign=sign
    

    def _init_from_string(self, name):
        if(len(self) != 4):
            raise ValueError
        self._init_from_list(self[0], self[1], self[2], self[3])

    
    def _init_from_pitches(self, pitch1, pitch2):
        pass
    

    def __str__(self):
        return f'Interval:'


    def __repr__(self):
        return f'Interval(\"\")'


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
        pass


    def string(self):
        pass


    def full_name(self, *, sign=True):
        quality = self.quality_name()
        if(quality=='ooooo'):
            quality = "quintuply-diminished"
        if(quality=='oooo'):
            quality = "quadruply-diminished"
        if(quality=='ooo'):
            quality = "triply-diminished"
        if(quality=='oo'):
            quality = "doubly-diminished"
        if(quality=='o'):
            quality = "diminished"
        if(quality=='m'):
            quality = "minor"
        if(quality=='P'):
            quality = "perfect"
        if(quality=='M'):
            quality = "major"
        if(quality=='+'):
            quality = "augmented"
        if(quality=='++'):
            quality = "doubly-augmented"
        if(quality=='+++'):
            quality = "triply-augmented"
        if(quality=='++++'):
            quality = "quadruply-augmented"
        if(quality=='+++++'):
            quality = "quintuply-augmented"


    def span_name(self):
        return _span_names[self.span]


    def quality_name(self):
        return _unsafe_qual_names[self.qual]


    def matches(self, other):
        pass


    def lines_and_spaces(self):
        pass


    def _to_iq(self, name):
        pass


    def to_list(self):
        pass


    def is_unison(self, qual=None):
        pass


    def is_second(self, qual=None):
        pass
    
    def is_third(self, qual=None):
        pass


    def is_fourth(self, qual=None):
        pass


    def is_fifth(self, qual=None):
        pass


    def is_sixth(self, qual=None):
        pass


    def is_seventh(self, qual=None):
        pass

    
    def is_octave(self, qual=None):
        pass


    def is_diminished(self):
        pass
    

    def is_minor(self):
        pass

    
    def is_perfect(self):
        pass

    
    def is_major(self):
        pass

    
    def is_augmented(self):
        pass

    
    def is_perfect_type(self):
        pass

    
    def is_imperfect_type(self):
        pass

        
    def is_simple(self):
        pass

        
    def is_compound(self):
        pass

    
    def is_ascending(self):
        pass

    
    def is_descending(self):
        pass

    
    def is_consonant(self):
        pass

                   
    def is_dissonant(self):
        pass

    
    def complemented(self):
        pass

    
    def semitones(self):
        pass

    
    def add(self, other):
        pass

    
    def transpose(self, p):
        pass


if __name__ == '__main__':
    # Add your testing code here!
    print("Testing...")

    print("Done")
    pass

