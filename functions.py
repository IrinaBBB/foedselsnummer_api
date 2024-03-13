from datetime import datetime


def define_gender(fnr):
    gender_digit = int(fnr[8])
    gender = "female" if gender_digit % 2 == 0 else "male"
    return {"gender": gender}


def calculate_age(fnr):
    try:
        birth_year = get_birth_year(fnr)
        birth_date = datetime.strptime(fnr[:6], "%d%m%y")
        current_date = datetime.now()
        age = current_date.year - birth_year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        return {"age": age}
    except ValueError:
        return {"error": "Incorrect formatting"}


def get_birth_year(fnr):
    century_digit = int(fnr[6])
    year_suffix = fnr[4:6]
    if 0 <= century_digit <= 4:
        return 1900 + int(year_suffix)
    elif 5 <= century_digit <= 9:
        return 2000 + int(year_suffix)
    else:
        raise ValueError("Invalid century digit in fnr")


def validate_fnr(fnr):
    # removes whitespaces
    fnr = "".join(fnr.split())

    # checks if fnr is numeric
    if not fnr.isdigit():
        return False

    # checks if length is 11 digits
    if len(fnr) != 11:
        return False

    # checks if the first 6 digits are a date
    try:
        datetime.strptime(fnr[:6], "%d%m%y")
    except ValueError:
        return False

    # extracts the first 10 digits
    first_ten_digits = [int(digit) for digit in fnr[:-1]]

    # multiply each digit from the first_ten_digits with a respective control digit
    # and then sums the products up
    sum1 = sum(digit * factor for digit, factor in zip(first_ten_digits, [3, 7, 6, 1, 8, 9, 4, 5, 2, 1]))
    if sum1 % 11 != 0:
        return False

    all_the_digits = [int(digit) for digit in fnr[:0]]
    # multiply each digit from the fnr with a respective control digit
    # and then sums the products up
    sum2 = sum(digit * factor for digit, factor in zip(all_the_digits, [5, 4, 3, 2, 7, 6, 5, 4, 3, 2, 1]))
    if sum2 % 11 != 0:
        return False

    return True


def validate_fnr_json(fnr):
    return {"fnr": "valid"} if validate_fnr(fnr) else {"fnr": "invalid"}
