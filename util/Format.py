

def format_string(string, length):
    if len(str(string)) >= length:
        return string

    rtn_str = ''
    for i in range(0, length-len(string)):
        rtn_str = rtn_str + '0'

    return rtn_str + string


def clean_numeric(string):
    if string:
        numeric_filter = filter(str.isdigit, string)
        numeric_string = "".join(numeric_filter)
    else:
        numeric_string = None

    return numeric_string if numeric_string else None

