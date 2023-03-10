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

# region Helper Functions


def isConstant(fx: str) -> bool:
    """Returns True if the function is a constant"""
    return True if fx.find('x') == -1 else False


def getDegree(fx: str) -> int:
    """
    Returns the degree of a function

    Constants return a degree of 0
    """
    return int(fx[fx.find('^')+1:]) if fx.find('^') != -1 else 0


def getCoefficient(fx: str) -> int:
    """Returns the coefficient"""
    if not isConstant(fx):
        return int(fx[:fx.find('x')]) if fx.find('x') > 0 else 1
    else:
        return int(fx)

# endregion

# region Diff Rules : Basics


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
            return '0'
        # Else, power rule
        else:
            # Calulates the new values of a and b
            ap = str(a * bNum) if a else b
            bp = '' if bNum == 2 else '^' + str(bNum - 1)

            return ap + "x" + bp

# endregion

# region String Manipulation


SYMBOL_LIST = ['+', '-', '*', '/']


def combine(fxs: list[str]) -> list[str]:
    """Simplifies the subfunctions by combining like terms"""
    # Simplify
    for i in range(len(fxs)):
        # Loop removes summed terms, so make sure i is in bounds
        if i >= len(fxs):
            break

        combined: list[str] = []
        currFx = fxs[i]

        # Combines all the possible terms
        for j in range(i+1, len(fxs)):
            if getDegree(currFx) == getDegree(fxs[j]):
                currCoef = getCoefficient(currFx)
                fxs[i] = str(currCoef + getCoefficient(fxs[j])) + \
                    currFx[currFx.find(str(currCoef))+1:]

                # Removes the combined terms later
                combined.append(fxs[j])

        # Removes all the terms that have been summed
        # Has to be done this way incase two are the same
        # i.e. 0-5=-5, double -5
        for gx in combined:
            fxs.remove(gx)

    # Sort off of degree and returns the sorted list
    # Negative exponents come before constants (constant degree == 0)
    return fxs


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

    # If there is a subtract symbol
    # make the following number negative
    # and set the symbol to addition
    for i in range(len(symbols)):
        if symbols[i] == '-':
            subFunctions[i + 1] = symbols[i] + subFunctions[i + 1]
            symbols[i] = '+'

    return (subFunctions, symbols)


def combineFunction(gPrimes: list[str], symbols: list[str]) -> str:
    """Combines the subfunctions"""

    fPrime: str = ""

    # Combine like terms
    gPrimes = combine(gPrimes)

    # Properly order the terms
    # Constant goes the the end
    gPrimes.sort(reverse=True, key=lambda x: getDegree(x)
                 if not isConstant(x) else float("-inf"))

    # Iterates through each dirived subfunction and concatinates them
    for i, e in enumerate(gPrimes):
        # Makes sure there is something in the string
        if e:
            # If there is a symbol in front of the subfunction, add the correct symbol

            if i > 0:
                if e[0] == '-':
                    fPrime += e if symbols[i - 1] == '+' else '+' + e[1:]
                else:
                    fPrime += symbols[i - 1] + e

            else:
                fPrime = e

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
        if not isConstant(gx):
            gPrimes.append(power(gx))

    # Create the complete derived function
    fPrime = combineFunction(gPrimes, g_s[1])

    return fPrime


print(derivative("2x^3+3x^0-5x^1-3x^3+x^-6-5"))
