import csv

# reads in a CSV file for inflation data between 1960 and 2019
def inflation_reader(dict):
    # read the csv file in
    with open('inflation_data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
    
        # sort values into a dictionary {key = year, value = amount}
        for row in csv_reader:
            dict[row['year']] = round(float(row['amount']), 2)

# calculate total percent change from one year to another
# includes error checking for year boundary condition
def calculate_pct_change(orig, inc, dct):

    # boundary condition
    if ((orig >= 1800 or orig <= 2019) and (inc >= 1800 or inc <= 2019)):
        _original = dct[str(orig)]
        increase = dct[str(inc)] - _original
        change = round((increase/_original) * 100.0, 2)
    else:
        return -999

    return change

def main():
    # dictionary to store CSV information
    inflation_dict = {}
    inflation_reader(inflation_dict)

    # prompt for user input
    original = input("Enter a year: ")

    # exit condition (input is -999)
    while (original != -999):

        # prompt for more information
        new_number = input("Enter another year: ")
        original_amount = input("Enter amount: $")

        # calculate total percent change
        change = calculate_pct_change(original, new_number, inflation_dict)
        decimal_change = change / 100.0

        # calculate total change between years for a given amount
        total_dollar = round((original_amount*decimal_change) + original_amount, 2)

        # check for exit
        if (change != -999):
            
            # print total change between years
            print("Total percent change from " + str(original) + " to " + str(new_number) + " is: " + str(change) + "%")
            print("$" + str(original_amount) + " from " + str(original) + " is worth about $" + str(total_dollar) + " in " + str(new_number))

        else:

            #print an error
            print("Make sure new_number enter a year between 1800 and 2019")

        # keep reading input
        original = input("Enter a year: ")


main()