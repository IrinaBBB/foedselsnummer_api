from datetime import datetime


def define_gender_json(fnr):
    gender_digit = int(fnr[8])
    gender = "female" if gender_digit % 2 == 0 else "male"
    return {"gender": gender}


def is_male(fnr):
    gender_digit = int(fnr[8])
    return gender_digit % 2 != 0


class InvalidFnrFormatError(Exception):
    pass


def calculate_age(fnr):
    try:
        print("fnr: {}".format(fnr))
        birth_year = get_birth_year(fnr)
        birth_date = datetime.strptime(fnr[:6], "%d%m%y")
        current_date = datetime.now()
        age = current_date.year - birth_year - (
                (current_date.month, current_date.day) < (birth_date.month, birth_date.day))
        print("age: {}".format(age))
        return age
    except ValueError:
        print("Error raised for value:", fnr)


def get_age_json(fnr):
    try:
        return {"age": calculate_age(fnr)}
    except InvalidFnrFormatError:
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


def read_file():
    values = []

    with open('db/fnr.txt', 'r') as file:
        for line in file:
            values.append(line.strip())
    return values


def check_if_fnr_in_dataset(fnr):
    with open('db/fnr.txt', 'r') as file:
        dataset = {line.strip() for line in file}

    if fnr in dataset:
        return {"result": "fnr is in dataset"}
    else:
        return {"result": "fnr is not found"}


def get_counts(fnr_list):
    total_count = 0
    male_count = 0
    female_count = 0

    for fnr in fnr_list:
        if validate_fnr(fnr):
            total_count += 1
            gender_male = is_male(fnr)
            if gender_male:
                male_count += 1
            else:
                female_count += 1

    return {"total_count": total_count, "male_count": male_count, "female_count": female_count}


def get_counts_by_gender_age():
    counts = {}

    with open('db/fnr.txt', 'r') as file:
        for line in file:
            fnr = line.strip()
            if validate_fnr(fnr):
                gender = "male" if is_male(fnr) else "female"
                age = calculate_age(fnr)
                age_group = calculate_age_group(age)

                counts.setdefault(gender, {}).setdefault(age_group, 0)
                counts[gender][age_group] += 1

    return counts


def calculate_age_group(age):
    age_groups = {
        "0-17": (float('-inf'), 17),
        "18-29": (18, 29),
        "30-49": (30, 49),
        "50-64": (50, 64),
        "65+": (65, float('inf'))
    }

    for group, (lower, upper) in age_groups.items():
        if lower <= age <= upper:
            return group
