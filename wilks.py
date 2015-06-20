"""
Author = Robert Ross Wardrup

A short wilks score powerlifting utility to record
and compare your wilks score to other lifters
 """


def coef(sex, weight):
    """
    Determines Wilk's coefficient - to be multiplied times weight
    lifted.
    :param sex: Lifter's sex
    :param weight: Lifter's bodyweight
    :return coef: Wilk's coefficient
    """

    w_coef = 0
    coefs = dict.fromkeys(['a', 'b', 'c', 'd', 'e', 'f'], 0)
    weight = int(weight)

    if sex == 'male':
        coefs['a'] = -216.0475144
        coefs['b'] = 16.2606339
        coefs['c'] = -0.002388645
        coefs['d'] = -0.00113732
        coefs['e'] = 7.01863E-06
        coefs['f'] = -1.291E-08

    elif sex == 'female':
        coefs['a'] = 594.31747775582
        coefs['b'] = -27.23842536447
        coefs['c'] = 0.82112226871
        coefs['d'] = -0.00930733913
        coefs['e'] = 0.00004731582
        coefs['f'] = -0.00000009054

    cs = sorted(coefs.items())
    a, b, c, d, e, f = [v[1] for v in cs]


    w_coef = 500 / (a + (b * weight) + (c * (weight ** 2)) + (d * (weight ** 3)) + (e * (weight ** 4))
                    + (f * (weight ** 5)))

    return w_coef


def wilkscore(total, coef):
    """
    Determine's Wilk's score based on lifter's total.
    :param total: Lifter's total weight lifted
    :return: Score of time int
    """

    total = int(total)
    score = total * coef

    return score


def calc():
    print("\nWilk's Calculator\n")
    sex = int(input("1. Male"
                    "\n2. Female"))
    if sex == 1:
        sex = 'male'
    elif sex == 2:
        raise NotImplementedError
    else:
        calc()
    weight = input("\nBody weight: ")
    total = input("\nTotal weight lifted: ")
    score = wilkscore(total, coef(sex, weight))
    print("\n** Your Wilk's score is {0} **".format(score))


if __name__ == '__main__':
    calc()
