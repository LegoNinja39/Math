"""
Used to simplify terms

Takes a function as a list of strings and a list of symbols
Operations within parentheses should be a sublist

Currently only supports single variable functions
"""

# Order of operations
SYMBOL_LIST = ['*', '/', '+', '-']


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


def simpleSign(fx: str, baseSign: str = '+') -> str:
    """
    Simplifies +/- signs when concatinating terms

    Return the correct sign
    """
    return '+' if baseSign == fx[0] else '-'


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


def simplifyFunction(gPrimes: list[str], symbols: list[str]) -> str:
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
                fPrime += simpleSign(e)

                if e[0] == '-':
                    fPrime += e if symbols[i - 1] == '+' else '+' + e[1:]
                else:
                    fPrime += symbols[i - 1] + e

            else:
                fPrime = e

    return fPrime
