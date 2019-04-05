from data_process import *
from matplotlib.ticker import PercentFormatter

MAX_GASPRICE = 200

def get_data_by_x_y(data,field_x,field_y,max_gas=MAX_GASPRICE):
    x = []
    y = []
    # Check the array is not empty and the input targetfield is valid
    if(len(data) > 0) and (field_x in data[0]) and (field_y in data[0]):
        for row in data:
            temp_x = row[field_x]
            temp_y = row[field_y]
            if(temp_x <= max_gas) and (temp_y <= float("inf")):
                x.append(temp_x)
                y.append(temp_y)
    else:
        print("input list is empty or invalid fields")
    
    return (x,y)    

def main():
    # Histogram of Gas price
    url = 'http://localhost:5000/waitingminedtime'
    data = get_data(url)
    x,y = get_data_by_x_y(data,'_id','value',5000)
    # x,y = get_data_by_x_y(data,'_id','value',5000)

    # x_index = []
    # for i in range(0,len(x)):
    #     x_index.append(i)
    # plt.scatter(x_index,np.log(x))
    # plt.hist(x, weights=np.ones(len(x)) / len(x))
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    # plt.title('Histogram of gas price')
    x2 = np.sort(x)
    y2 = np.arange(len(x2))/float(len(x2))
    plt.plot(x2, y2)
    plt.title('Probability distribution of gas price')
    plt.xlabel('gas price')
    plt.ylabel('distribution of gas price')
    plt.show()
    
    # Scatter plot waiting mined time/ hist gram of waiting mined time
    url = 'http://localhost:5000/waitingminedtime'
    data = get_data(url)
    x,y = get_data_by_x_y(data,'_id','value')
    plt.scatter(x,np.log(y))
    plt.ylabel('log of waiting mined time')
    plt.xlabel('gas price')
    plt.legend()
    plt.show()

    # Scatter plot waiting time of all data
    url = 'http://localhost:5000/gasstat'
    data = get_data(url)
    x,y = get_data_by_x_y(data,'_id','value')
    plt.scatter(x,np.log(y))
    plt.ylabel('log of waiting time')
    plt.xlabel('gas price')
    plt.legend()
    plt.show()
    return

if __name__== "__main__":
    main()