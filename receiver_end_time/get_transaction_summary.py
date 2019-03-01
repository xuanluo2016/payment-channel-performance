from datetime import datetime
# the time lag between Etherscan server and local server
TIMEZONE_DELTA = 0

def extract_digit(str):
    """
    extract only digits from a string
    """
    return [int(s) for s in str.split() if s.isdigit()]

def remove_redundant_characters(str, char1, char2):
    """
    remove substrings before and after two characters
    exmaple:
    input: '12@[123]57'. '[',']'
    output: '[123]'
    """
    left_index = str.find(char1)
    right_index = str.find(char2)
    result = str[left_index: (right_index +1)]
    return result

def remove_redundant_characters2(str, char1, char2):
    """
    remove substrings before and after two characters
    exmaple:
    input: '12@[123]57'. '[',']'
    output: '123'
    """
    left_index = str.find(char1)
    right_index = str.find(char2)
    result = str[left_index: right_index]
    return result

def get_end_time(item):
    """
    extract the end time from item, which contains a field called 'timestamp'
    return None if item is empty or timestamp is empty, else return timestamp(time format)
    """
    try:
        time = item['timestamp']
        # remove special characters in timestamp
        time = remove_redundant_characters(time, '(', ')')
        time = time[1: len(time)-len("+UTC")-1]
        return parser.parse(time)
    except Exception as e:
        return None


def get_transction_fee(item):
    """
    extract the actual gas fee from item, which contains a filed called 'actual_cost'
    return None if item is empty or actual_cost is empty, else return actual_cost(str)
    """
    try:
        actual_cost = item['actual_cost']
        # remove special characters in actual_cost
        actual_cost = remove_redundant_characters2(actual_cost, '', 'Ether')
        return actual_cost
    except Exception as e:
        return None

def get_gas_price(item):
    """
    extract the actual gas fee from item, which contains a filed called 'actual_cost'
    return None if item is empty or gas_price is empty, else return gas_price (float)
    """
    try:
        gas_price = item['gas_price']
        # remove special characters in actual_cost
        gas_price = remove_redundant_characters2(actual_cost, '', 'Ether')
        gas_price = float(gas_price)
        gas_price = gas_price * 1000000000
        return gas_price
    except Exception as e:
        return None

def get_summary(item, txhash, start_time, end_time):
    print(item)
    print(txhash)

    if(start_time != None) and (end_time != None):
        try:
            end_time = int(end_time, 16)
            # end_time = datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            end_time = datetime.utcfromtimestamp(end_time)

            print(start_time)
            print(end_time)
            print(type(start_time))
            print(type(end_time))
            waiting_time = end_time - start_time
            print(waiting_time)
            actual_cost = get_transction_fee(item)
            print(actual_cost)
            gas_price = get_gas_price(item)

            item = {"txhash": txhash, "waitingtime": waiting_time, "actualcost": actual_cost, "gas_price":gas_price}        
            return item
        except:
            return None