#############################################################################################################
#
#  Homework 1 (Python Intro)
#  Types, Loops, Conditionals, Functions
#
#  Instructions:
#    * for each of the functions below, read the docstring and implement the function as described.
#
#    * feel free to to add helper functions, but DO NOT MODIFY the descriptions of the original functions.
#
#    * absolutely NO import statements should be added, they will result in an automatic 0 (the autograder
#    will break)
#
#    * Some functions specify that certain built in functions may not be used. BE MINDFUL OF THIS.
#
#    * If for whatever reason, an implementation detail is unclear, feel free to email for clarification.
#
#    * Have Fun!
#
#############################################################################################################

def power(base, exp):
    """
    Implement the math.pow function for integer powers. Note: exp can still be negative. This should be
    handled properly. What other edge cases should we be careful of? Return base^exp as a float.

    THIS IMPLEMENTATION SHOULD NOT USE: math.pow(base, exp) or base ** exp

    :param base: number to raise to a given power
    :type base: int
    :param exp: power to raise the base to. NOTE: this number can be negative!
    :type exp: int
    :return: base to the exp power
    :rtype: float
    """
    # replace the line below with your code
    output = float(1)
    for i in range(abs(exp)):
        output *= base
    if exp >= 0:
        return output
    else:
        return 1 / output


def list_sum(l):
    """
    given a list l, return the sum of all the elements of l. You can assume that l only contains ints & floats.

    :param l: list of floats/ints
    :type l: list
    :return: the sum of all the elements in l, AS A FLOAT
    :rtype: float
    """
    # replace the line below with your code
    output = 0.0
    for element in l:
        output += element
    return output

def str_to_int(num_string):
    """
    Turn a string into an integer. For this function, num_string can be a string representation of a number in either
    binary, octal, decimal, or hexadecimal. Depending on the base, the string will start differently:
        binary:      "0b100" = 4 "0b" is first 2 characters
        octal:       "0o11"  = 9 "0o" is first 2 characters
        decimal:     "10"    = 10 no extra characters
        hexadecimal: "0xa"   = 10
     For binary, octal, and hexadecimal, the string will always be longer than 2 (i.e. the base prefix, and then the
     number. No matter the base, you are to correctly convert the string to an int and return it.

     If the base is unrecognized (the first two are not numbers, and also are not '0b', '0o', or '0x', the function
     should return -1.

    Don't worry about negative numbers!

    **hint** remember that the int() function can take multiple parameters. What was that second parameter?

    :param num_string: string representation of the integer
    :type num_string: str
    :return: integer with the value represented in the string, or negative one if the base is unrecognized
    :rtype: int
    """
    # replace the line below with your code
    if len(num_string) < 2:
        return -1
    if len(num_string) == 2:
        return int(num_string)
    if num_string[0 : 2] == "0b":
        return int(num_string, 2)
    if num_string[0 : 2] == "0o":
        return int(num_string, 8)
    if num_string[0 : 2] == "0x":
        return int(num_string, 16)
    return -1

def print_christmas_tree(size):
    """
    A christmas tree with size n is defined as a string having n + 1 rows, where the i'th row contains the (i-1)'th row's
    number of stars + 2, arranged in a symmetrical manner. the 0'th row should have 1 star. the last (n'th) row should
    be equivalent to the 0'th row (the trunk of the tree). the stars are asterisks: '*'. size is always >= 2.

    Example of a size 4 tree:
       *
      ***
     *****
    *******
       *

    The return should be a single string, with each row separated by '\n'. Mind the spacing in each row--there should
    be spaces before the '*'s on each row, but not after.

    size 4 tree as string:
        "   *\n  ***\n *****\n*******\n   *"

    **hint** print out your tree to the console a few times to make sure the spacing is correct.

    :param size: a number >=2
    :type size: int
    :return: string representation of a christmas tree
    :rtype: str
    """
    # replace the line below with your code
    output = ""
    for i in range(size):
        for spaces in reversed(range(size - i - 1)):
            output += " "
        output = christmas_tree_helper(i, output)
    for last_row_spaces in reversed(range(size - 1)):
        output += " "
    output += "*"
    return output

def christmas_tree_helper(row, str):
    num_stars = 2*row + 1
    for i in range(num_stars):
        str += "*"
    str += "\n"
    return str

def list_to_str(l):
    """
    Implement the __str()__ function for the list class. This function should take a list, and convert
    it to its string representation. You can assume that for each element in the list, the str() function
    will give the appropriate string to use for the entire list string. Some examples of list strings:
        [1, 2, 3, 4, 5, 6]
        [True, False, True, True, False]
        ['hi', 'my', 'name', 'is']

    * NOTICE: for string elements, the string itself is surrounded by single quotes. You are expected to
              implement this. this is the only special case you should be aware of
    * you will not be graded on the spacing of your string representation, i.e. [1,2,3] == [1, 2, 3] == [ 1, 2, 3 ]
    * you can assume that there will be no nested lists/dictionaries/tuples nested in the list
    * do NOT assume that all elements in the list are of the same type

    * YOU ARE EXPECTED TO USE str() FOR EACH ELEMENT IN THE LIST
    * DO NOT USE str() ON THE LIST ITSELF

    :param l: list to convert to string
    :type l: list
    :return: string representation of that list
    :rtype: str
    """
    # replace the line below with your code
    output = "["
    for item in l:
        if isinstance(item, str):
            output += "'" + str(item) + "', "
        else:
            output += str(item) + ", "
    output = output.strip(', ')
    output += "]"
    return output


def remove_substring_instances(in_str, substr):
    """
    given the string input, find all instances of substr and remove them from the input. Then, return the number of
    instances of substr that were removed, as well as the new string with all instances of substr removed, as a tuple.
    for example:
        return num_instances, new_string

    :param in_str: string to clean up
    :type in_str: str
    :param substr: substring to find and remove
    :type substr: str
    :return: a tuple where the first element is the number of elements removed, and the second is the string after
        cleaning
    :rtype: tuple
    """
    # replace the line below with your code
    num_instances = 0
    new_string = ""
    current_word = ""
    for char in in_str:
        if (char == ' ' or char == ',' or char == '.'):
            if (current_word == substr):
                print(current_word)
                num_instances += 1
                current_word = ""
                new_string += char
            else:
                new_string += current_word
                current_word = ""
                new_string += char
        else:
            current_word += char
    return num_instances, new_string

def main():
    print(list_to_str([1, 2, 3, 4]))
main()