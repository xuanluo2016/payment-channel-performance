# extract only digits from a string
def extract_digit(str):
    return [int(s) for s in str.split() if s.isdigit()]

# remove substrings before and after two characters
# exmaple:
# input: '12@[123]57'. '[',']'
# output: '[123]'
def remove_redundant_characters(str, char1, char2):
    left_index = str.find(char1)
    right_index = str.find(char2)
    result = str[left_index: (right_index +1)]
    return result