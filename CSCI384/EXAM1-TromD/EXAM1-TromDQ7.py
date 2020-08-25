"""
Derek Trom
EXAM1 Q9
Optional implementation
"""
import itertools
import sys as system

def get_value(word, substitution):

    s = 0
    factor = 1
    for letter in reversed(word):
        s += factor * substitution[letter]
        factor *= 10
    return s


def solve2(equation):

    # split equation in left and right
    left, right = equation.lower().replace(' ', '').split('=') # split by = sign
    # split words in left part
    left = left.split('+')
    # create list of used letters
    letters = set(right)
    for word in left:
        for letter in word:
            letters.add(letter)
    letters = list(letters)
    #possible digits
    digits = range(10)
    # loop until the right permutation is found for it to be equal
    for perm in itertools.permutations(digits, len(letters)):
        sol = dict(zip(letters, perm)) #mapping numbers to letters
        #if sum on the left side == sum on the right side for current mapping
        if sum(get_value(word, sol) for word in left) == get_value(right, sol):
            print(' + '.join(str(get_value(word, sol)) for word in left) + " = {} \n(mapping: {})".format(get_value(right, sol), sol))
            return True
    return False

if __name__ == '__main__':
    found = solve2('EUROPA + MARS + URANUS = SATURN')
    if found == False:
        print("No solution found")
        system.exit(0)

    system.exit(0)
