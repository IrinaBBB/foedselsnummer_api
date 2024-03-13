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
    except ValueError as e:
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
