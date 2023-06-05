import math
from flask import flash, render_template

""" CREDIT CARD """
def check_credit_card(card):
    card = int(card)

    number_02 = math.floor(((card % pow(10, 2)) / pow(10, 1)))
    number_04 = math.floor(((card % pow(10, 4)) / pow(10, 3)))
    number_06 = math.floor(((card % pow(10, 6)) / pow(10, 5)))
    number_08 = math.floor(((card % pow(10, 8)) / pow(10, 7)))
    number_10 = math.floor(((card % pow(10, 10)) / pow(10, 9)))
    number_12 = math.floor(((card % pow(10, 12)) / pow(10, 11)))
    number_14 = math.floor(((card % pow(10, 14)) / pow(10, 13)))
    number_16 = math.floor(((card % pow(10, 16)) / pow(10, 15)))

    number_02 = number_02 * 2
    number_04 = number_04 * 2
    number_06 = number_06 * 2
    number_08 = number_08 * 2
    number_10 = number_10 * 2
    number_12 = number_12 * 2
    number_14 = number_14 * 2
    number_16 = number_16 * 2

    final_n_02 = math.floor((number_02 % pow(10, 2)) / 10 + (number_02 % pow(10, 1)))
    final_n_04 = math.floor((number_04 % pow(10, 2)) / 10 + (number_04 % pow(10, 1)))
    final_n_06 = math.floor((number_06 % pow(10, 2)) / 10 + (number_06 % pow(10, 1)))
    final_n_08 = math.floor((number_08 % pow(10, 2)) / 10 + (number_08 % pow(10, 1)))
    final_n_10 = math.floor((number_10 % pow(10, 2)) / 10 + (number_10 % pow(10, 1)))
    final_n_12 = math.floor((number_12 % pow(10, 2)) / 10 + (number_12 % pow(10, 1)))
    final_n_14 = math.floor((number_14 % pow(10, 2)) / 10 + (number_14 % pow(10, 1)))
    final_n_16 = math.floor((number_16 % pow(10, 2)) / 10 + (number_16 % pow(10, 1)))

    sum_second_last = (final_n_02 + final_n_04 + final_n_06 + final_n_08 + final_n_10 + final_n_12 + final_n_14 + final_n_16)

    number_01 = math.floor((card % pow(10, 1)))
    number_03 = math.floor((card % pow(10, 3)) / pow(10, 2))
    number_05 = math.floor((card % pow(10, 5)) / pow(10, 4))
    number_07 = math.floor((card % pow(10, 7)) / pow(10, 6))
    number_09 = math.floor((card % pow(10, 9)) / pow(10, 8))
    number_11 = math.floor((card % pow(10, 11)) / pow(10, 10))
    number_13 = math.floor((card % pow(10, 13)) / pow(10, 12))
    number_15 = math.floor((card % pow(10, 15)) / pow(10, 14))

    sum_remainder = (number_01 + number_03 + number_05 + number_07 + number_09 + number_11 + number_13 + number_15)

    final_sum = (sum_second_last + sum_remainder)

    VISA16 = math.floor((card % pow(10, 16)) / pow(10, 15))
    VISA13 = math.floor((card % pow(10, 13)) / pow(10, 12))
    MASTER = math.floor((card % pow(10, 16)) / pow(10, 14))
    AMEX = math.floor((card % pow(10, 15)) / pow(10, 13))

    if ((final_sum % 10 == 0 and VISA16 == 4)):
        return True
    elif ((final_sum % 10 == 0 and VISA13 == 4)):
        return True
    elif ((final_sum % 10 == 0 and (MASTER >= 51 and MASTER <= 55)) or (final_sum % 10 == 0 and (MASTER == 22))):
        return True
    elif ((final_sum % 10 == 0 and (AMEX == 34 or AMEX == 37))):
        return True
    else:
        return False