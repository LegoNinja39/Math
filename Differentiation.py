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
            return ''
        # Else, power rule
        else:
            # Calulates the new values of a and b
            ap = str(a * bNum) if a else b
            bp = '' if bNum == 2 else '^' + str(bNum - 1)

            return ap + "x" + bp

# endregion

# region String Manipulation


SYMBOL_LIST = ['+', '-', '*', '/']


def combine(fxs: list[str]):
    """
    Simplifies the subfunctions by combining like terms

    Returns an ordered list based on degree
    """

    # Simplify
    for i in range(len(fxs)):
        # Loop removes summed varibles, so make sure i is in bounds
        if i >= len(fxs):
            break

        combined: list[str] = []
        currFx = fxs[i]

        # Combines all the possible varibles
        for j in range(i+1, len(fxs)):
            if getDegree(currFx) == getDegree(fxs[j]):
                currCoef = getCoefficient(currFx)
                fxs[i] = str(currCoef + getCoefficient(fxs[j])) + \
                    currFx[currFx.find(str(currCoef))+1:]
                combined.append(fxs[j])

        # Removes all the varibles that have been summed
        fxs = [e for e in fxs if e not in combined]

    # Sort off of degree and returns the sorted list
    # Negative exponents come before constants (constant degree == 0)
    return sorted(fxs, reverse=True, key=lambda x: getDegree(x) if not isConstant(x) else float("-inf"))


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


def combineFunction(gPrimes: list[str], symbols: list[str]) -> str:
    """Combines the subfunctions"""

    fPrime: str = ""

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
        if not isConstant(gx):
            gPrimes.append(power(gx))

    # Create the complete derived function
    fPrime = combineFunction(gPrimes, g_s[1])

    return fPrime


# print(derivative("2x^3+3x^0-5x^1+x^-6-5"))
print(combine(splitFunction("2x^3+3x^0-5x^1+3x^3+x^-6-5")[0]))
