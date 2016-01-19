"""
Author = Robert Ross Wardrup

A short wilks score powerlifting utility to record
and compare your wilks score to other lifters
 """

import csv
import numpy as np
import scipy as sp
import scipy.stats

#TODO: Enable Z-score printing to create a ranking system
#TODO: Incorporate code from openpowerlifting tool

csvPath = './data/openpowerlifting.csv'  # Data file

def unitConvert(number):
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
        weight = unitConvert(weight)

    #w_coef = 0
    coefs = dict.fromkeys(['a', 'b', 'c', 'd', 'e', 'f'], 0)

    if sex == 'M':
        coefs['a'] = -216.0475144
        coefs['b'] = 16.2606339
        coefs['c'] = -0.002388645
        coefs['d'] = -0.00113732
        coefs['e'] = 0.00000701863
        coefs['f'] = -0.00000001291

    elif sex == 'F':
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

    w_coef = 500 / (a + (b * weight) + (c * weight ** 2) + (d * weight ** 3) +
                    (e * weight ** 4) + (f * weight ** 5))

    return w_coef


def wilkScore(units, total, coef):
    """
    Determine's Wilk's score based on lifter's total.
    :param total: Lifter's total weight lifted
    :return: Score of time int
    """
    if units == 'lbs':
        total = unitConvert(total)

    total = float(total)
    score = total * coef

    return score


def fRange(x, y):
    step = 0.01
    r = []
    while x < y:
        x += step
        r.append(x)
    return r

def filter(csvpath, sex, weight):
    """
    parse powerlifting results based on sex, gear, age, etc.
    Uses output from https://github.com/sstangl/openpowerlifting
    :param csvpath: Path to CSV file containing meet results
    :param reqs: a dict of requested lifter characteristics (sex, age class,
    weight class, equipped, division)
    :return:
    """

    weight1 = 0
    weight2 = 0
    wilks = []
    weight = int(unitConvert(weight))
    division = 0

    #TODO: Find a better method for setting up these ranges, to allow floats

    if sex == "M":
        division = "Open Men"
        if weight in range(0, 59):
            weight1 = 53
            weight2 = 58.99
        elif weight in range(59, 66):
            weight1 = 59
            weight2 = 65.99
        elif weight in range(66, 74):
            weight1 = 66
            weight2 = 73.99
        elif weight in range(74, 83):
            weight1 = 74
            weight2 = 82.99
        elif weight in range(83, 93):
            weight1 = 83
            weight2 = 92.99
        elif weight in range(93, 105):
            weight1 = 93
            weight2 = 104.99
        elif weight in range(105, 120):
            weight1 = 105
            weight2 = 119.99
        elif weight in range(120, 99999):
            weight1 = 120
            weight2 = 99999

    elif sex == 'F':
        division = "Open Women"
        if weight in range(0, 47):
            weight1 = 53
            weight2 = 58.99

        elif weight in range(47, 52):
            weight1 = 47
            weight2 = 51.99

        elif weight in range(52, 57):
            weight1 = 52
            weight2 = 56.99

        elif weight in range(57, 63):
            weight1 = 57
            weight2 = 62.99

        elif weight in range(63, 72):
            weight1 = 63
            weight2 = 71.99

        elif weight in range(72, 84):
            weight1 = 72
            weight2 = 83.99

    print("You're in the {0}k weight class.".format(weight1))  # Print weight class

    with open(csvPath, "rt") as csvFile:
        dataReader = csv.reader(csvFile)
        count = 0
        equip = "Raw"  # Filter only raw lifters
        for row in dataReader:
            try:
                float(row[5])
                validWc = True  # Check weight class
            except ValueError:
                validWc = False
                pass  # This is not ideal.
            if validWc:
                if row[15] and row[2]:
                    if row[2] == "{0}".format(division):
                        if row[3] == "{0}".format(sex) \
                        and row[4] == "{0}".format(equip) \
                        and float(row[5]) >= float(weight1) \
                        and float(row[5]) <= float(weight2):
                            w = float(row[15])
                            wilks.append(w)

                    count += 1
    return wilks


def mean_ci(data, confidence=0.95):
    """
    Calculate mean and confidence intervals for Wilk's scores
    :param data:
    :param confidence:
    :return:
    """
    if len(data) == 0:
        raise ValueError
    else:
        a = 1.0*np.array(data)
        n = len(a)
        m, se = np.mean(a), scipy.stats.sem(a)
        h = se * sp.stats.t._ppf((1 + confidence) / 2., n-1)

        p25, p50, p75 = np.percentile(data, 25), np.percentile(data, 50), \
                        np.percentile(data, 75)

    return m, m-h, m+h, p25, p50, p75


def wilks_target(sex, weight):
    """
    Runs an estimation at current weight to determine total needed for
    competitive wilks score.
    :return:
    """
    wilks = filter(csvPath, sex, weight)
    if len(wilks) == 0:  # If the filter returns an empty line, error out
        raise ValueError
    else:
        mean, lc, hc, p25, p50, p75 = mean_ci(wilks)
        total = 0
        w = 0
        total_ath = len(wilks)

        while w < p75:  # iterate through totals until your Wilks exceeds the expected value (p75)
            w = wilkScore('lbs', total, coef('lbs', sex, weight))
            total += 1

    print("\nBased on {0} observations.. In order to obtain a competitive score "
          "at your bodyweight, you'd need to lift a total of {1} lbs, "
          "for a wilk's score of {2} points.".
          format(total_ath, total,round(w, 2)))

    input("\nPress enter to return to main menu.")
    main_menu()


def main_menu():
    print("Powerlifting Tools\n"
          "Main Menu\n\n"
          "1. Calculate Wilks Score\n"
          "2. Compare Wilks Score\n"
          "3. Estimate required total\n")
    answer = int(input(">>> "))
    if answer == 1:
        calc()

    elif answer == 2:
        print("1. Male\n"
              "2. Female")
        sex = int(input(">>> "))
        if sex == 1:
            sex = 'M'
        elif sex == 2:
            sex = 'F'

        weight = float(input("\nEnter weight in lbs: "))

        total = float(input(("\nEnter total weight lifted in lbs: ")))

        score = round(wilkScore('lbs', total, coef('lbs', sex, weight)), 2)
        wilks = filter(csvPath, sex, weight)
        athletes = len(wilks)
        mean, lc, hc, p25, p50, p75 = mean_ci(wilks)

        print("\nMean Wilk's Score: {0}, out of {1} observations.".
              format(round(mean, 2), athletes))
        print("The 95% confidence interval lies between {0} and {1}".
              format(round(lc, 2), round(hc, 2)))
        print("Median Wilk's Score: {0}".format(round(p50, 2)))
        print("The upper and lower quartiles are {0} and {1}".
              format(p25, p75))
        print("\n\nYour Wilk's score is {0}".format(score))

        score = int(score)
        lc = int(lc)
        hc = int(hc)
        p25, p50, p75 = int(p25), int(p50), int(p75)

        if score in range(lc, hc):
            print("Your score, {0}, is within the confidence interval of "
                  "{1} to {2} points.".format(score, lc, hc))
        elif score in range(hc, 99999):
            print("Your score, {0}, is above the confidence interval {1} "
                  "points. You should compete!".format(score, hc))
        if score in range(p25, p50):
            print("Your score is in the 25th percentile of lifts, {0} to "
                  "{1} points.".format(p25, p50))
        elif score in range(p50, p75):
            print("Your score is in the 75th percentile of lifts, {0} to "
                  "{1} points. You should compete!"
                  .format(p50, p75))
        elif score > p75:
            print("Your score is above the 75th percentile, {0}. You should compete!"
                  .format(p75))

        input("\nPress enter to return to main menu")
        main_menu()

    elif answer == 3:
        print("Sex:\n"
              "1. Male\n"
              "2. Female\n")
        sex = int(input((">>> ")))
        if sex == 1:
            sex = 'M'
        elif sex == 2:
            sex = 'F'
        print("Body weight: \n")
        weight = int(input(">>> "))

        wilks_target(sex, weight)

    else:
        main_menu()


def calc():
    print("\nWilk's Calculator\n")
    print("1. Lbs"
          "\n2. Kg\n")
    unit = int(input("\n>>> "))
    if unit == 1:
        unit = "lbs"
    elif unit == 2:
        unit = "kg"
    print("\n1. Male"
                    "\n2. Female")
    sex = int(input("\n>>> "))
    if sex == 1:
        sex = 'M'
    elif sex == 2:
        sex = 'F'
    else:
        calc()

    print("\nBody weight: ")
    weight = float(input("\n>>> "))
    print("\nTotal weight lifted: ")
    total = float(input("\n>>> "))
    score = round(wilkScore(unit, total, coef(unit, sex, weight)), 2)
    print("\n** Your Wilk's score is {0} **".format(score))
    input("\n Press enter to return to calculation input screen.")
    calc()

if __name__ == '__main__':
    main_menu()
