"""
Author = Robert Ross Wardrup

A short wilks score powerlifting utility to record
and compare your wilks score to other lifters
 """
import csv
from numpy import genfromtxt

csvpath = './data/openpowerlifting.csv'

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


def filter(csvpath, critereon):
    """
    parse powerlifting results based on sex, gear, age, etc.
    Uses output from https://github.com/sstangl/openpowerlifting
    :param csvpath: Path to CSV file containing meet results
    :param reqs: a dict of requested lifter characteristics (sex, age class, weight class, equipped, division)
    :return:
    """
    # TODO - When athlete is listed multiple times, only use highest wilks score in statistics
    columns = ['Name', 'Place', 'Division', 'Sex', 'Equipment', 'WeightClassKg', 'BodyweightKg', 'Age', 'BestSquatKg',
               'BestBenchKg', 'BestDeadliftKg', 'TotalKg', 'Wilks', 'McCulloch']

    with open(csvpath, "rt") as csvfile:
        datareader = csv.reader(csvfile)
        count = 0
        sex = "M"
        wclass = "74.84"
        age = "28"
        name = []
        for row in datareader:
            if row[15]:
                if row[3] == "{0}".format(sex) and row[5] == "{0}".format(wclass) and row[7] == "{0}".format(age):
                    _name = str(row[0])
                    if _name in name:
                        wilk = float(0)
                        _wilk = float(row[15])
                        while wilk < _wilk:
                            wilk = float(row[15])
                        if row[15] == wilk:
                            yield row
                            count += 1
                    else:
                        name.append(_name)
                        yield row
                        count += 1

                elif count < 10000:
                    continue
                else:
                    return


def parser_csv(csvpath):
    """
    Parse CSV after filtering
    :param csvpath:
    :return:
    """
    criteria = ["M", '74.84', '28']
    for critereon in criteria:
        for row in filter(csvpath, critereon):
            yield row


def main_menu():
    print("Powerlifting Tools\n"
          "Main Menu\n\n"
          "1. Calculate Wilks Score\n"
          "2. Compare Wilks Score\n")
    answer = int(input(">>> "))
    if answer == 1:
        calc()
    elif answer == 2:
        for row in parser_csv(csvpath):
            print(row)
    else:
        main_menu()

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
    input("\n Press enter to return to calculation input screen.")
    calc()

if __name__ == '__main__':
    main_menu()
