# extract only digits from a string
def extract_digit(str):
    return [int(s) for s in str.split() if s.isdigit()]