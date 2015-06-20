"""
Author = Robert Ross Wardrup

A short wilks score powerlifting utility to record
and compare your wilks score to other lifters
 """

def unitconvert(number):
    """
    Converts lbs to kg
    :param number: Number to convert
    :return: float, in kg
    """

    return number * 0.453592


def coef(units, sex, weight):
    """
    Determines Wilk's coefficient - to be multiplied times weight
    lifted.
    :param units: Kilograms or Lbs
    :param sex: Lifter's sex
    :param weight: Lifter's bodyweight
    :return coef: Wilk's coefficient
    """
    if units == "lbs":
        weight = unitconvert(weight)

    w_coef = 0
    coefs = dict.fromkeys(['a', 'b', 'c', 'd', 'e', 'f'], 0)

    if sex == 'male':
        coefs['a'] = -216.0475144
        coefs['b'] = 16.2606339
        coefs['c'] = -0.002388645
        coefs['d'] = -0.00113732
        coefs['e'] = 0.00000701863
        coefs['f'] = -0.00000001291

    elif sex == 'female':
        coefs['a'] = 594.31747775582
        coefs['b'] = -27.23842536447
        coefs['c'] = 0.82112226871
        coefs['d'] = -0.00930733913
        coefs['e'] = 0.00004731582
        coefs['f'] = -0.00000009054

    else:
        raise ValueError

    cs = sorted(coefs.items())
    a, b, c, d, e, f = [v[1] for v in cs]

    w_coef = 500 / (a + (b * weight) + (c * weight ** 2) + (d * weight ** 3) + (e * weight ** 4)
                    + (f * weight ** 5))

    return w_coef


def wilkscore(units, total, coef):
    """
    Determine's Wilk's score based on lifter's total.
    :param total: Lifter's total weight lifted
    :return: Score of time int
    """
    if units == 'lbs':
        total = unitconvert(total)

    total = float(total)
    score = total * coef

    return score


def calc():
    print("\nWilk's Calculator\n")
    print("1. Lbs"
          "\n2. Kh\n")
    unit = int(input("\n>>> "))
    if unit == 1:
        unit = "lbs"
    elif unit == 2:
        unit = "kg"
    print("\n1. Male"
                    "\n2. Female")
    sex = int(input("\n>>> "))
    if sex == 1:
        sex = 'male'
    elif sex == 2:
        sex = 'female'
    else:
        calc()

    print("\nBody weight: ")
    weight = float(input("\n>>> "))
    print("\nTotal weight lifted: ")
    total = float(input("\n>>> "))
    score = round(wilkscore(unit, total, coef(unit, sex, weight)), 2)
    print("\n** Your Wilk's score is {0} **".format(score))


if __name__ == '__main__':
    calc()
