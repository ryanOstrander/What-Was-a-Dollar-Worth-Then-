import csv

def calculate_pct_change(orig, inc, dct):

    # boundary condition
    if ((orig >= 1800 or orig <= 2019) and (inc >= 1800 or inc <= 2019)):
        _original = dct[str(orig)]
        increase = dct[str(inc)] - _original
        change = round((increase/_original) * 100.0, 2)
    else:
        return -999

    return change

def calculate_dollar_change(start_year, end_year, original_amount, dct):

    #retrieve
    start_year_inflation = dct[str(start_year)]

    #find difference in inflation between two years
    inflation_diff = dct[str(end_year)] - start_year_inflation

    #calculate total percent change between
    inflation_pct_change = round((inflation_diff/start_year_inflation) * 100.0, 2)

    #convert to decimal
    inflation_decimal_change = inflation_pct_change / 100.0

    #convert original monetary value and round to nearest tenth place
    converted_money_value = round((original_amount*inflation_decimal_change) + original_amount, 2)

    return converted_money_value

def inflation_reader(dict):
    # read the csv file in
    with open('/home/ryanOst/mysite/inflation_data.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # sort values into a dictionary {key = year, value = amount}
        for row in csv_reader:
            dict[row['year']] = round(float(row['amount']), 2)