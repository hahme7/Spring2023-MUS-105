###############################################################################
# ratio.py : A class that implements fractional numbers.
# See ratio.html for module documentation.

from math import gcd, pow
from decimal import Decimal
from collections import namedtuple


# A namedtuple base class for Ratio with num and den properties.
RatioBase = namedtuple('RatioBase', ['num', 'den'])


class Ratio (RatioBase):
    def __new__(cls, num, den=None):
        isint = lambda n: isinstance(n, int)
        isfloat = lambda n: isinstance(n, float)
        isstr = lambda n: isinstance(n, str)
        if den == 0:
            raise ZeroDivisionError
        if isint(num):
            if isinstance(den, int):
                if(den < 0 and num < 0):
                    den = abs(den)
                    num = abs(num)
                elif(den < 0):
                    den = abs(den)
                    num = -num
                greatest = gcd(num, den)
                num /= greatest
                den /= greatest
                return super().__new__(cls, int(num), int(den))
            else:
                return super().__new__(cls, int(num), 1)
        elif isfloat(num):
            if(den != None):
                raise TypeError
            temp = Decimal(str(num)).as_integer_ratio()
            num = temp[0]
            den = temp[1]
            greatest = gcd(num, den)
            num /= greatest
            den /= greatest
            return super().__new__(cls,int(num),int(den))
        elif isstr(num):
            tempList = num.split('/')
            num = int(tempList.pop(0))
            den = int(tempList.pop())
            if(den < 0 and num < 0):
                den = abs(den)
                num = abs(num)
            elif(den < 0):
                den = abs(den)
                num = -num
            greatest = gcd(num, den)
            num /= greatest
            den /= greatest
            return super().__new__(cls, int(num), int(den))
        else:
            raise TypeError

    def __str__(self):
        return f"Ratio: {self.num}/{self.den}"


    def __repr__(self):
        return f'Ratio("{self.num}/{self.den}")'


    def __mul__(self, other):
        if(isinstance(other, Ratio)):
            return Ratio(self.num*other.num, self.den*other.den)
        if(isinstance(other, int)):
            return Ratio(self.num*other, self.den)
        if(isinstance(other, float)):
            as_float = self.num / self.den
            return Ratio(as_float*other)
        raise TypeError

    
    # Implements right side multiplication (same code as __mul__)
    __rmul__ = __mul__


    def __truediv__(self, other):
        if(isinstance(other, Ratio)):
            other = other.reciprocal()
            return Ratio(self.num*other.num, self.den*other.den)
        if(isinstance(other, int)):
            return Ratio(self.num, self.den*other)
        if(isinstance(other, float)):
            return (self.num / self.den) / other
        raise TypeError


    def __rtruediv__(self, other):
        if(isinstance(other, int)):
            recip = self.reciprocal()
            return Ratio(recip.num * other, recip.den)
        if(isinstance(other, float)):
            recip = self.reciprocal()
            return other * (recip.num / recip.den)
        raise TypeError

    
    def __invert__(self):
        if (not isinstance(self, Ratio) and not isinstance(self, int) and not isinstance(self, float)):
            raise TypeError
        return self.reciprocal(self)


    def __add__(self, other):
        if(isinstance(other, Ratio)):
            lcm = self.lcm(self.den, other.den)
            self_num = self.num*(lcm/self.den)
            other_num = other.num*(lcm/other.den)
            return Ratio(int(self_num+other_num), lcm)
        elif(isinstance(other, int)):
            other *= self.den
            return Ratio(self.num+other, self.den)
        elif(isinstance(other, float)):
            return (self.num/self.den)+other
        raise TypeError




    
    # Implements right side addition (same code as __add__)
    __radd__ = __add__


    def __neg__(self):
        return Ratio(-self.num, self.den)
    

    def __sub__(self, other):
        if(isinstance(other, Ratio)):
            lcm = self.lcm(self.den, other.den)
            self_num = self.num*(lcm/self.den)
            other_num = other.num*(lcm/other.den)
            return Ratio(int(self_num-other_num), lcm)
        if(isinstance(other, int)):
            other *= self.den
            return Ratio(self.num-other, self.den)
        if(isinstance(other, float)):
            return (self.num / self.den) - other
    

    def __rsub__(self, other):
        if(isinstance(other, int)):
            other *= self.den
            return Ratio(other-self.num, self.den)
        if(isinstance(other, float)):
            return other - (self.num / self.den)
        raise TypeError


    def __mod__(self, other):
        first_mod = self.num*other.den
        sec_mod = other.num*self.den
        modded_num = first_mod%sec_mod
        return Ratio(modded_num,self.lcm(self.den, other.den))


    def __pow__(self, other):
        if(isinstance(other, int)):
            return Ratio(self.num**other, self.den**other)
        if(isinstance(other, Ratio)):
            num = self.num**other.num
            den = self.den**other.num
            num = num**(1/other.den)
            den = den**(1/other.den)
            return num/den
        if(isinstance(other, float)):
            return (self.num / self.den) ** other
        raise TypeError


    def __rpow__(self, other):
        if(isinstance(other, int) or isinstance(other, float)):
            return other ** (self.num / self.den)


    def __lt__(self, other):
        if (self.compare(other) < 0):
            return True
        return False

    
    def __le__(self, other):
        if (self.compare(other) <= 0):
            return True
        return False

    
    def __eq__(self, other):
        return self.compare(other) == 0


    def __ne__(self, other):
        if(isinstance(other, Ratio)):
            return self.compare(other) != 0
        return self.compare(Ratio(other)) != 0


    def __ge__(self, other):
        if (self.compare(other) >= 0):
            return True
        return False


    def __gt__(self, other):
        if (self.compare(other) > 0):
            return True
        return False


    def __hash__(self):
        return hash(Ratio(self.num, self.den+16))
    

    def compare(self, other):
        if (isinstance(other, Ratio)):
            return (self.num * other.den) - (other.num * self.den)
        if (isinstance(other,int) or isinstance(other, float)):
            other = Ratio(other)
            return (self.num * other.den) - (other.num * self.den)
        raise TypeError 


    @staticmethod
    def lcm(a, b):
        return (a*b) // gcd(a,b)

    
    def string(self):
        return f"{self.num}/{self.den}"


    def reciprocal(self):
        return Ratio(self.den, self.num)


    def dotted(self, dots=1):
        if(dots <= 0):
            raise ValueError
        count = Ratio(self.num,self.den)
        for i in range(dots):
            count = count.__truediv__(2)
            self += count 
        return self


    def tuplets(self, num, intimeof=1):
        output = []
        for i in range(num):
            output.append(self.__truediv__(num).__mul__(intimeof))
        return output


    def tup(self, num):
        if(not isinstance(num, int)):
            raise ValueError
        temp = self.__truediv__(num)
        return tuple((temp.num,temp.den))


    def float(self):
        return float(self.num / self.den)


    def seconds(self, tempo=60, beat=None):
        if(beat is None):
            beat = Ratio(1,4)
        if(not isinstance(beat, Ratio)):
            raise TypeError
        num_beats_per_sec = float(tempo / 60)
        beat_per_sec = beat.__mul__(num_beats_per_sec)
        return self.__truediv__(beat_per_sec).float()



if __name__ == '__main__':
    print("Testing...")
    print(Ratio(11,12)>=0.7)
    print("Done!")
