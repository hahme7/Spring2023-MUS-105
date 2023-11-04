"""
Implement an Enum called ScaleDegrees, where each scale degree enumeration will encode two different concepts:

a degree, one of: SD1, SD2, SD3, SD4, SD5, SD6, SD7
an inflection, one of: LOWERED, DIATONIC, RAISED.

Directions:
Your Enum will define enumerations for the 7 degrees SD1...SD7, with values 0,2,4,5,7,9,11 that represent the scale degree's number of half-steps up from the tonic note.

Your class will define enumerations for the 3 inflections LOWERED, DIATONIC, RAISED, with values -1, 0, 1.

For each degree and inflection you will then define a 'scale degree enumeration' whose value is a tuple (degree, inflection). Since there are 7 degrees and 3 infections for each degree there will be a total of 21 enumerations. Each enumeration name will be the concatenation of the inflection and step names e.g. LOWERED_TONIC, TONIC, RAISED_TONIC, and so on.

In addition, your ScaleDegree enum will provide three methods:

degree() returns the degree-only enumeration of the scale degree.
inflection() returns the inflection-only value of the scale degree.
semitones() returns the semitonal content of the scale degree. The 7 diatonic versions of the degrees have the semitonal content [0, 2, 4, 5, 7, 9, 11]; lowered inflections reduce diatonic semitones by 1 and raised inflections add 1 to the diatonic semitones.
"""

from enum import Enum, IntEnum, auto

class ScaleDegrees (Enum):
    # define the seven degrees here, the first one is given to you.
    SD1 = 0
    SD2 = 2
    SD3 = 4
    SD4 = 5
    SD5 = 7
    SD6 = 9
    SD7 = 11

    # define the three inflections here, the first one is given to you.
    LOWERED = -1
    DIATONIC = 0
    RAISED = 1

    # define the twenty-one scale steps here. The seven diatonic scale degree
    # names are:  TONIC SUPERTONIC MEDIANT SUBDOMINANT DOMINANT SUBMEDIANT LEADINGTONE.
    # The very first scale degree step is given to you:
    LOWERED_TONIC = (SD1, LOWERED)
    TONIC = (SD1, DIATONIC)
    RAISED_TONIC = (SD1, RAISED)

    LOWERED_SUPERTONIC = (SD2, LOWERED)
    SUPERTONIC = (SD2, DIATONIC)
    RAISED_SUPERTONIC = (SD2, RAISED)
    
    LOWERED_MEDIANT = (SD3, LOWERED)
    MEDIANT = (SD3, DIATONIC)
    RAISED_MEDIANT = (SD3, RAISED)

    LOWERED_SUBDOMINANT = (SD4, LOWERED)
    SUBDOMINANT = (SD4, DIATONIC)
    RAISED_SUBDOMINANT = (SD4, RAISED)

    LOWERED_DOMINANT = (SD5, LOWERED)
    DOMINANT = (SD5, DIATONIC)
    RAISED_DOMINANT = (SD5, RAISED)

    LOWERED_SUBMEDIANT = (SD6, LOWERED)
    SUBMEDIANT = (SD6, DIATONIC)
    RAISED_SUBMEDIANT = (SD6, RAISED)
    
    LOWERED_LEADINGTONE = (SD7, LOWERED)
    LEADINGTONE = (SD7, DIATONIC)
    RAISED_LEADINGTONE = (SD7, RAISED)
    

    def degree(self):
        """Returns the degree enum for this enum.
        Hint: the first tuple value of this enum
        will be the value of the degree enum."""
        return self.value[0]

    def inflection(self):
        """Returns the inflection enum for this enum.
        Hint: the second tuple value of this enum
        will be the value of the inflection enum."""
        return self.value[1]
    
    def semitones(self):
        """Returns the number of semitones in this
        scale degree.  Hint: Use the values of degrees
        and inflectons to determine the semitonal content"""
        return self.degree() + self.inflection()



if __name__ == "__main__" :
    # Degree
    ScaleDegrees['SD1']

    # Inflection
    ScaleDegrees['LOWERED']
    
    # ScaleDegree
    ScaleDegrees['TONIC']

    # Returns the degree enum of a scale degree
    print(ScaleDegrees['RAISED_SUPERTONIC'].degree())

    # Returns the degree enum of a scale degree
    print(ScaleDegrees['LOWERED_SUPERTONIC'].degree())

    # Returns the number of semitones in a scale degree
    print(ScaleDegrees['LOWERED_DOMINANT'].semitones())


    

