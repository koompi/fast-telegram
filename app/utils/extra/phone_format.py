import re


def clear_phone_format(phone):
    clean_phone_number = re.sub('[^0-9]+', '', phone)
    formatted_phone_number = f"+{clean_phone_number}"
    return formatted_phone_number
