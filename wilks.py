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

    coef = 0
    weight = int(weight)
    if sex == 'male':
        coef = 500 / (216.0475144 + (16.2606339 * weight) +
                      (0.002388645 * weight ** 2) +
                      (-0.002388645 * weight ** 3) + (7.01863 * 10 ** -6)
                      + (-1.291 * 10 ** -8))
    print(coef)

    return coef


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
