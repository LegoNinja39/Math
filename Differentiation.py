"""
Finds the dirivtive of a function
    Currently only can find single variable derivatives
    Currently only works for independent variables
    Assumes to find for x
    Assumes integers
    Assumes Real solution

    Legal Symbols:
        x : var
        0-9 : numbers
        + : add
        - : sub
        * : mul
        / : div
        ^ : exp
"""

# region Diff Rules : Basics

# First check


def constant(fx: str) -> bool:
    """Returns True if the function is a constant"""
    return True if fx.find('x') == -1 else False

# Second check


def power(fx: str) -> str:
    """Takes the function ax^b and returns the derivative as a string"""
    # Seperate the string into its parts
    x = fx.find('x')
    a = int(fx[:x]) if x > 0 else 0

    # 2 needs to be added to get to the other side of the ^
    # Makes sure the string isn't empty later
    b = fx[x+2:]

    # If there is no exponent, just return the coefficeint
    if not b:
        return str(a)

    else:
        bNum = int(b)

        # If the exponent is 1, remove x
        if bNum == 1:
            return str(a)
        # If the exponent is 0, x == 1 and it's a constant
        elif bNum == 0:
            return ''
        # Else, power rule
        else:
            # Calulates the new values of a and b
            ap = str(a * bNum) if a else b
            bp = '' if bNum == 2 else '^' + str(bNum - 1)

            return ap + "x" + bp

# endregion

# region Parsing


SYMBOL_LIST = ['+', '-', '*', '/']


def splitFunction(fx: str) -> tuple[list[str], list[str]]:
    """Parses the function"""

    lastSubIndex = 0
    subFunctions: list[str] = []
    symbols: list[str] = []

    # Find all the subfunctions
    for i, e in enumerate(fx):
        # When it finds an algebraic symbol
        if SYMBOL_LIST.count(e) != 0 and fx[i-1].isnumeric():
            # Puts the subfunctions and symbols into lists
            subFunctions.append(fx[lastSubIndex:i])
            symbols.append(fx[i:i+1])

            lastSubIndex = i + 1

    # Gets the last subfuction
    subFunctions.append(fx[lastSubIndex:])

    return (subFunctions, symbols)


def combineFunction(gPrimes: list[str], symbols: list[str]):
    """Combines the subfunctions"""

    fPrime: str = ""
    print(gPrimes)
    # Iterates through each dirived subfunction and concatinates them
    for i, e in enumerate(gPrimes):
        # Makes sure there is something in the string
        if e:
            # If there is a symbol in front of the subfunction, add the correct symbol
            fPrime += symbols[i - 1] + e if i > 0 else e

    return fPrime

# endregion


def derivative(fx: str) -> str:
    """Finds the derivative"""

    # Get all the subfunctions
    g_s = splitFunction(fx)
    gxes = g_s[0]

    gPrimes: list[str] = []

    # Derive every subfunction
    for gx in gxes:
        if not constant(gx):
            gPrimes.append(power(gx))

    # Create the complete derived function
    fPrime = combineFunction(gPrimes, g_s[1])

    return fPrime


print(derivative("2x^3+3x^0-5x^1+x^-6-5"))
