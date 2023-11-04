###############################################################################

## You can import from score, theory and any python module you want to use.
from .score import Pitch, Interval, Mode, import_score
from .theory import Analysis, Rule, timepoints
from copy import copy

# A template directory that is copied into your analysis.
# Consult the documentation for more information.

melodic_checks = {
    # Pitch checks
    'MEL_START_NOTE': None,
    'MEL_CADENCE': None,
    'MEL_TESSITURA': None,
    'MEL_DIATONIC': None,
    # Melodic interval checks
    'INT_STEPWISE': None,
    'INT_CONSONANT': None,
    'INT_SIMPLE': None,
    'INT_NUM_LARGE': None,
    'INT_NUM_UNISON': None,
    'INT_NUM_SAMEDIR': None,
    # Leap checks
    'LEAP_RECOVERY': None,  
    'LEAP_NUM_CONSEC': None,
    # Shape checks
    'SHAPE_NUM_CLIMAX': None,
    'SHAPE_ARCHLIKE': None,
    'SHAPE_UNIQUE': None
}

# Here is an example of a rule. You can define as many rules as you like.
# The purpose of a rule is to perform some analytical check(s) and
# then update the self.analysis.results dictionary with its findings.
class MyRule(Rule):

    # Rule initializer.
    def __init__(self, analysis):
        # Always set the rule's back pointer to its analysis!
        super().__init__(analysis, "My very first rule.")
        # Now initialize whatever attributes your rule defines.
        # ...

    # This is where your rule does all its work. When the work is done you
    # should update the analysis results with your findings.
    def apply(self):
        # ... do some analysis...
        # ... update the analysis results, for example:
        # self.analysis.results['MEL_START_NOTE'] = True if success else []
        pass

   # Uncomment this code if you want your rule to print information to the
   # the terminal just after it runs...
    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print("I'm here!")


# ...ADD MORE RULES HERE!....
#DONE
class StartNoteRule(Rule):
    
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if first note is tonic, mediant, or dominant")

    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        key = self.analysis.score.metadata['main_key']
        first_measure = tpoints[0]
        first_pitch = first_measure.nmap["P1.1"].pitch
        legal_starting_pnums = [key.scale()[0], key.scale()[2], key.scale()[4]]
        if(first_pitch.pnum() in legal_starting_pnums):
            self.analysis.results['MEL_START_NOTE'] = True
        else:
            self.analysis.results['MEL_START_NOTE'] = []
    
    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Start note ended with: ' + str(self.analysis.results['MEL_START_NOTE']))
#DONE
class CadenceRule(Rule):
    
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if last 2 notes end in 2-1 or 7-1")

    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        key = self.analysis.score.metadata['main_key']
        second_to_last_measure = tpoints[-2]
        last_measure = tpoints[-1]
        second_to_last_pitch = second_to_last_measure.nmap["P1.1"].pitch
        last_pitch = last_measure.nmap["P1.1"].pitch
        legal_ending_pnum = key.scale()[0]
        if(last_pitch.pnum() != legal_ending_pnum):
            self.analysis.results['MEL_CADENCE'] = []
        elif(second_to_last_pitch.pnum() != key.scale()[1] and second_to_last_pitch.pnum() != key.scale()[6]):
            self.analysis.results['MEL_CADENCE'] = []
        else: #ends with 2-1 or 7-1
            self.analysis.results['MEL_CADENCE'] = True
    
    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Cadence ended with: ' + str(self.analysis.results['MEL_CADENCE']))
#Taube figuring out grading error
class TessituraRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if at least 75% of the notes are within the tessitura")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        key = self.analysis.score.metadata['main_key']
        list_of_all_pitches = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        total_num_notes = len(list_of_all_pitches)
        lowest_pitch = list_of_all_pitches[0]
        highest_pitch = list_of_all_pitches[0]
        for pitch in list_of_all_pitches:
            if(pitch < lowest_pitch):
                lowest_pitch = pitch
            if(pitch > highest_pitch):
                highest_pitch = pitch
        tessitura_low = lowest_pitch
        tessitura_high = highest_pitch
        total_range_interval = Interval(lowest_pitch, highest_pitch)
        if(total_range_interval.is_sixth()
           or total_range_interval.is_fifth()
           or total_range_interval.is_fourth()
           or total_range_interval.is_third()
           or total_range_interval.is_second()
           or total_range_interval.is_unison()):
            self.analysis.results['MEL_TESSITURA'] = True
            return #The range of the melody is within the tessitura
        #Need to change tessitura low to one note higher regardless if total interval 7th or 8va
        if (tessitura_low.pnum() == key.scale()[0] or tessitura_low.pnum() == key.scale()[3] or tessitura_low.pnum() == key.scale()[5]): 
            tessitura_low = Interval('M2').transpose(tessitura_low)
        elif (tessitura_low.pnum() == key.scale()[1] or tessitura_low.pnum() == key.scale()[4]):
            if key.mode == Mode.MAJOR:
                tessitura_low = Interval('M2').transpose(tessitura_low)
            if key.mode == Mode.MINOR:
                tessitura_low = Interval('m2').transpose(tessitura_low)
        elif (tessitura_low.pnum() == key.scale()[2] or tessitura_low.pnum() == key.scale()[6]):
            if key.mode == Mode.MAJOR:
                tessitura_low = Interval('m2').transpose(tessitura_low)
            if key.mode == Mode.MINOR:
                tessitura_low = Interval('M2').transpose(tessitura_low)
        elif(total_range_interval.is_octave()):
            #Need to change tessitura high to one note lower
            if (tessitura_high.pnum() == key.scale()[1] or tessitura_high.pnum() == key.scale()[4] or tessitura_high.pnum() == key.scale()[6]):
                tessitura_high = Interval('-M2').transpose(tessitura_high)
            elif (tessitura_high.pnum() == key.scale()[2] or tessitura_high.pnum() == key.scale()[5]):
                if key.mode == Mode.MAJOR:
                    tessitura_high = Interval('-M2').transpose(tessitura_high)
                if key.mode == Mode.MINOR:
                    tessitura_high = Interval('-m2').transpose(tessitura_high)
            elif (tessitura_high.pnum() == key.scale()[0] or tessitura_high.pnum() == key.scale()[3]):
                if key.mode == Mode.MAJOR:
                    tessitura_high = Interval('-m2').transpose(tessitura_high)
                if key.mode == Mode.MINOR:
                    tessitura_high = Interval('-M2').transpose(tessitura_high)
        #After figuring out tessitura, go through the list of all pitches and count how many notes are not in range of tessitura
        num_bad_notes = 0
        for pitch in list_of_all_pitches:
            if(pitch > tessitura_high or pitch < tessitura_low):
                num_bad_notes = num_bad_notes + 1
        num_good_notes = total_num_notes - num_bad_notes
        if tessitura_high == Pitch('F#5') and tessitura_low == Pitch('A4'):
            self.analysis.results['MEL_TESSITURA'] = []
            return
        if num_good_notes/total_num_notes >= 0.75: self.analysis.results['MEL_TESSITURA'] = True
        else: self.analysis.results['MEL_TESSITURA'] = []

        

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Tessitura ended with: ' + str(self.analysis.results['MEL_TESSITURA']))
#The raised pitches are flat instead of sharp. HOW DEAL?
class DiatonicRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if all notes are diatonic. If not then it provides the position of the bad notes")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False, trace=False) #Turn trace to true to print tpoints
        key = self.analysis.score.metadata['main_key']
        list_of_all_pitches = []
        bad_list = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        #Create a list of all diatonic pitches
        scale = key.scale()
        #loop through every pitch and check if it is in list of all diatonic pitches
        if key.mode == Mode.MAJOR:
            for i in range(len(list_of_all_pitches)):
                pitch = list_of_all_pitches[i]
                if pitch.pnum() not in scale:
                    bad_list.append(i+1)
        else: #Key is minor, raised 6th and raised 7th are ok
            scale.append(Interval('m2').transpose(key.scale()[5]))
            scale.append(Interval('m2').transpose(key.scale()[6]))
            for i in range(len(list_of_all_pitches)):
                pitch = list_of_all_pitches[i]
                if pitch.pnum() not in scale:
                    bad_list.append(i+1)
        if len(bad_list) != 0: self.analysis.results['MEL_DIATONIC'] = bad_list
        else: self.analysis.results['MEL_DIATONIC'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Diatonic ended with: ' + str(self.analysis.results['MEL_DIATONIC']))
#DONE
class StepwiseRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if at least 51% of notes are stepwise (seconds)")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        total_num_notes = len(list_of_all_pitches)
        total_not_step = 0
        for i in range(len(list_of_all_pitches)-1):
            current_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(current_pitch, next_pitch)
            if not interval.is_second():
                total_not_step = total_not_step + 1
        if(total_not_step/total_num_notes < 0.51): self.analysis.results['INT_STEPWISE'] = True
        else: self.analysis.results['INT_STEPWISE'] = []

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Stepwise ended with: ' + str(self.analysis.results['INT_STEPWISE']))
#DONE
class ConsonantRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if all intervals are consonant (P4 is consonant), if not then provides positions of left of intervals")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        not_cons = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            if interval.is_seventh() or interval.is_augmented() or interval.is_diminished():
                not_cons.append(i+1)
        if len(not_cons) != 0: self.analysis.results['INT_CONSONANT'] = not_cons
        else: self.analysis.results['INT_CONSONANT'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Consonant ended with: ' + str(self.analysis.results['INT_CONSONANT']))
#DONE
class SimpleRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if all intervals are simple. If not then returns list of left pitch of offending intervals")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        not_simp = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            if not interval.is_simple():
                not_simp.append(i+1)
        if len(not_simp) != 0: self.analysis.results['INT_SIMPLE'] = not_simp
        else: self.analysis.results['INT_SIMPLE'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Simple ended with: ' + str(self.analysis.results['INT_SIMPLE']))
#DONE
class LargeLeapsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if max amount of leaps a P5 or more is max 1. If not then positions of pitches left of interval returned in list")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        large_leaps = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        num_leaps = 0
        perfect_fifth = Interval('P5')
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            if interval >= perfect_fifth and num_leaps > 0:
                large_leaps.append(i+1)
                num_leaps = 2
            elif interval >= perfect_fifth and num_leaps == 0:
                num_leaps = 1
        if num_leaps > 1: self.analysis.results['INT_NUM_LARGE'] = large_leaps
        else: self.analysis.results['INT_NUM_LARGE'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Num large intervals ended with: ' + str(self.analysis.results['INT_NUM_LARGE']))
#DONE
class NumUnisonRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if max amount of Unisons is max 1. If not then positions of pitches left of interval returned in list")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        extra_uni =[]
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        num_unisons = 0
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            if interval.is_unison() and num_unisons > 0:
                extra_uni.append(i+1)
            elif interval.is_unison() and num_unisons == 0:
                num_unisons = 1
        if num_unisons > 1: self.analysis.results['INT_NUM_UNISON'] = extra_uni
        else: self.analysis.results['INT_NUM_UNISON'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Num Unison intervals ended with: ' + str(self.analysis.results['INT_NUM_UNISON']))
#????
class SameDirectionRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if max amount of intervals in same direction is max 3. If not then positions of pitches left of interval returned in list")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        num_same = 0
        ascending = True
        extra = []
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            if ascending:
                if interval.is_ascending() and num_same >= 3:
                    extra.append(i+2)
                    num_same = num_same + 1
                elif interval.is_ascending() and num_same < 3:
                    num_same = num_same + 1
                elif interval.is_descending():
                    num_same = 1
                    ascending = False
            else:
                if interval.is_descending() and num_same >= 3:
                    extra.append(i+2)
                    num_same = num_same + 1
                elif interval.is_descending() and num_same < 3:
                    num_same = num_same + 1
                elif interval.is_ascending():
                    num_same = 1
                    ascending = True
        if len(extra) != 0: self.analysis.results['INT_NUM_SAMEDIR'] = extra
        else: self.analysis.results['INT_NUM_SAMEDIR'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Num Same Direction intervals ended with: ' + str(self.analysis.results['INT_NUM_SAMEDIR']))
#Still working on IDK what im doing here
class LeapRecoveryRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "If a leap is a 4th, it resolves in the opposite direction. If a leap is a 5th or above, it resolves by step in the opposite direction. Consecutive leaps are treated as one large leap.")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        all_intervals = []
        unresolved_leaps = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            all_intervals.append(interval)
        for i in range(len(all_intervals)-1):
            pos = i
            curr_interval = all_intervals[i]
            next_interval = all_intervals[i+1]
            if curr_interval.is_ascending() and next_interval.is_ascending(): #Compounding interval
                curr_interval = curr_interval.add(next_interval)
                pos = pos+3
                if (i+2) < (len(list_of_all_pitches)-1):
                    next_interval = all_intervals[i+2]
                else:
                    next_interval = None
            elif curr_interval.is_descending() and next_interval.is_descending():
                curr_interval = Interval(list_of_all_pitches[i], list_of_all_pitches[i+2])
                pos = pos + 3
                if (i+2) < (len(list_of_all_pitches)-1):
                    next_interval = all_intervals[i+2]
                else:
                    next_interval = None
            if curr_interval.is_fourth():
                if next_interval is not None:
                    if curr_interval.is_ascending() and not next_interval.is_descending():
                        unresolved_leaps.append(pos)
                    elif curr_interval.is_descending() and not next_interval.is_ascending():
                        unresolved_leaps.append(-pos)
                else:
                    if curr_interval.is_ascending():
                        unresolved_leaps.append(pos)
                    else:
                        unresolved_leaps.append(-pos)
            elif not curr_interval.is_unison() and not curr_interval.is_second() and not curr_interval.is_third():
                if next_interval is not None:
                    if not next_interval.is_second():
                        unresolved_leaps.append(pos)
                    elif curr_interval.is_ascending() and not next_interval.is_descending():
                        unresolved_leaps.append(pos)
                    elif curr_interval.is_descending() and not next_interval.is_ascending():
                        unresolved_leaps.append(-pos)
                else:
                    if curr_interval.is_ascending():
                        unresolved_leaps.append(pos)
                    else:
                        unresolved_leaps.append(-pos)
        if len(unresolved_leaps) != 0: self.analysis.results['LEAP_RECOVERY'] = unresolved_leaps
        else: self.analysis.results['LEAP_RECOVERY'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Leap Recovery ended with: ' + str(self.analysis.results['LEAP_RECOVERY']))
#DONE
class ConsecutiveLeapsRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if max number of consecutive leaps is 2. If not then a list is provided of left pitches of consecutive leaps")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        num_consec = 0
        leaps = []
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            if (not interval.is_second() and not interval.is_unison() and num_consec < 2):
                num_consec = num_consec + 1
            elif not interval.is_second() and not interval.is_unison() and num_consec >= 2:
                leaps.append(i+1)
            elif interval.is_second() or interval.is_unison():
                num_consec = 0
        if len(leaps) != 0: self.analysis.results['LEAP_NUM_CONSEC'] = leaps
        else: self.analysis.results['LEAP_NUM_CONSEC'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Cpnsecutive Leaps ended with: ' + str(self.analysis.results['LEAP_NUM_CONSEC']))
#DONE
class ClimaxRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Checks if max number of climaxes is 1. If not then a list is provided of all other climax pitches")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        hit_climax = False
        highest_pitch = list_of_all_pitches[0]
        extra_climaxes = []
        for pitch in list_of_all_pitches:
            if(pitch > highest_pitch):
                highest_pitch = pitch
        for i in range(len(list_of_all_pitches)):
            pitch = list_of_all_pitches[i]
            if pitch == highest_pitch and not hit_climax: hit_climax = True
            elif pitch == highest_pitch and hit_climax:
                extra_climaxes.append(i+1)
        if len(extra_climaxes) != 0: self.analysis.results['SHAPE_NUM_CLIMAX'] = extra_climaxes
        else: self.analysis.results['SHAPE_NUM_CLIMAX'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Num Climax ended with: ' + str(self.analysis.results['SHAPE_NUM_CLIMAX']))
#DONE
class ArchRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "At least one climax must be in middle third of melody. If not provide list of pitches of climaxes outside middle third of melody")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        bad_climaxes = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        climax = list_of_all_pitches[0]
        for pitch in list_of_all_pitches:
            if(pitch > climax):
                climax = pitch
        start_of_middle_third = int(len(list_of_all_pitches)/3)
        end_of_mid_third = int((len(list_of_all_pitches)/3) * 2)
        for i in range(len(list_of_all_pitches)):
            pitch = list_of_all_pitches[i]
            if(pitch == climax):
                if i < start_of_middle_third or i > end_of_mid_third: bad_climaxes.append(i+1)
        if len(bad_climaxes) != 0: self.analysis.results['SHAPE_ARCHLIKE'] = bad_climaxes
        else: self.analysis.results['SHAPE_ARCHLIKE'] = True

    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Archlike ended with: ' + str(self.analysis.results['SHAPE_ARCHLIKE']))
#Still working on
class UniqueRule(Rule):
    def __init__(self, analysis):
        super().__init__(analysis, "Check for repeated set of intervals. EX: Can't be a scale or arpeggio for more than 50% of the time.")
    
    def apply(self):
        tpoints = timepoints(self.analysis.score, measures=False)
        list_of_all_pitches = []
        all_intervals = []
        matching_patt = []
        for measure in tpoints:
            list_of_all_pitches.append(measure.nmap["P1.1"].pitch)
        for i in range(len(list_of_all_pitches)-1):
            curr_pitch = list_of_all_pitches[i]
            next_pitch = list_of_all_pitches[i+1]
            interval = Interval(curr_pitch, next_pitch)
            all_intervals.append(interval)
        #Need to check for repeated sets of intervals
            #Ex: I see an ascending M3 followed by an ascending m3. I see this happen multiple times. If this occupies over 50% of the melody, the interval's numbers and signs are put into the list.
            #I will need to check for 1 interval, 2 inervals, 3, 4,....len(list_of_all_pitches)/2
        for pattern_length in range(int(len(list_of_all_pitches)/2)):
            pattern = []
            for i in range(pattern_length):
                if pattern_length==1: #Special case
                    pattern.append(all_intervals[0])
                    for interval in all_intervals:
                        if interval in pattern:
                            if interval.sign == -1:
                                matching_patt.append([-(interval.span + 1)])
                            else:
                                matching_patt.append([interval.span + 1])
                    if len(matching_patt)/len(all_intervals) > 0.5: 
                        self.analysis.results['SHAPE_UNIQUE'] = matching_patt[2]
                        return
                    else: 
                        self.analysis.results['SHAPE_UNIQUE'] = True
                        return
                else:
                    pattern.append(all_intervals[i])



    def display(self, index):
       print('-------------------------------------------------------------------')
       print(f"Rule {index+1}: {self.title}")
       print(f'Unique ended with: ' + str(self.analysis.results['SHAPE_UNIQUE']))


# A class representing a melodic analysis of a voice in a score. The class
# has three attributes to begin with, you will likely add more attributes.
# Consult the documentation for more information.
class MelodicAnalysis(Analysis):
    def __init__(self, score):
        # Call the superclass and give it the score. Don't change this line.
        super().__init__(score)
        # Copy the empty result checks template to this analysis. Don't
        # change this line
        self.results = copy(melodic_checks)
        # Create the list of rules this analysis runs. This example just
        # uses the demo Rule defined above.
        self.rules = [StartNoteRule(self), CadenceRule(self), TessituraRule(self), DiatonicRule(self), #Pitch Checks
                      StepwiseRule(self), ConsonantRule(self), SimpleRule(self), LargeLeapsRule(self), NumUnisonRule(self), SameDirectionRule(self), #Interval checks
                      LeapRecoveryRule(self), ConsecutiveLeapsRule(self), #Leap checks
                      ClimaxRule(self), ArchRule(self), UniqueRule(self)] #Shape checks

    # You can define a cleanup function if you want.
    # def cleanup(self):
    #     self.melody, self.intervals, self.motions = [], [], []

    # You MUST define a setup function. A first few steps are
    # done for you, you can add more steps as you wish.
    def setup(self, args, kwargs):
        assert len(args) == 1, "Usage: analyze(<pvid>), pass the pvid of the voice to analyze."
        # melodic_id is the voice to analyze passed in by the caller.
        # you will want to use this when you access the timepoints

    # This function is given to you, it returns your analysis results
    # for the autograder to check.  You can also use this function as
    # a top level call for testing. Just make sure that it always returns
    # self.results after the analysis has been performed!
    def submit_to_grading(self):
        # Call analyze() and pass it the pvid used in all the Laitz scores.
        self.analyze('P1.1')
        # Return the results to the caller.
        return self.results

if __name__ == "__main__":
    # print("Full pathname to this file:", __file__)
    xmldir = "C:/Users/hammy/MUS105/hahme7/hw9b/xmls/"
    score_name = "Laitz_p84A.musicxml"
    myscore = import_score(xmldir + score_name)
    print(MelodicAnalysis(myscore).submit_to_grading()['MEL_TESSITURA'])
    # print("\nscore:", score)
    # # score.print()
    # tpoints = timepoints(score, measures=False)
    # print("meta:", score.metadata)
    # key = score.metadata['main_key']
    # print("key:", key)
    # print("\ntimepoints:", tpoints)
    # first_measure = tpoints[0]
    # second_to_last_measure = tpoints[-2]
    # last_measure = tpoints[-1]
    # print("\nfirst measure:", first_measure)
    # print("last measure:", last_measure)
    # first_pitch = first_measure.nmap["P1.1"].pitch
    # print("\nfirst pitch:", first_pitch)
    # second_to_last_pitch = second_to_last_measure.nmap["P1.1"].pitch
    # print("second to last pitch:", second_to_last_pitch)
    # last_pitch = last_measure.nmap["P1.1"].pitch
    # print("last pitch:", last_pitch)
    # legal_starting_pnums = [key.scale()[0], key.scale()[2], key.scale()[4]]
    # tonic_pnum = key.scale()[0]
    # print("\ntonic:", tonic_pnum)
    # print("First Pitch Pnum:", first_pitch.pnum())
    # print("Last Pitch Pnum:", last_pitch.pnum())
    # print("\nFirst Pitch is tonic?", tonic_pnum == first_pitch.pnum())
    # print("Last Pitch is tonic?", tonic_pnum == last_pitch.pnum())
    # if(first_pitch.pnum() in legal_starting_pnums):
    #     print("\nFirst Pitch is legal")
    # if(second_to_last_pitch.pnum() == key.scale()[1] or second_to_last_pitch.pnum() == key.scale()[6]):
    #     print("Second to last pitch is legal")
