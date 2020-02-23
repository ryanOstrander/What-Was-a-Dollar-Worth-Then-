#import statements
from flask import Flask, request, render_template
from processing import calculate_pct_change
from processing import inflation_reader
from processing import calculate_dollar_change

#create an instance of the flask application
app = Flask(__name__)
app.config["DEBUG"] = True

#set "/" link for GET and POST methods
@app.route("/", methods=["GET", "POST"])
def calculate_dollar():
    errors = ""

    #if the user attempts a post request
    if request.method == "POST":

        number1 = None
        number2 = None
        original_amount = None
        dct = {}

        #check for errors in form input
        try:
            number1 = int(request.form["number1"])
        except:
            errors += '''
            <div class="alert alert-dismissible alert-danger">
                <button type="button" class="close" data-dismiss="alert">×</button>
                <strong>Oh snap!</strong> <a href="#" class="alert-link">{!r} is not a number.</a>.
             </div>
             '''.format(request.form["number1"])
        try:
            number2 = int(request.form["number2"])
        except:
            errors += '''
            <div class="alert alert-dismissible alert-danger">
                <button type="button" class="close" data-dismiss="alert">×</button>
                <strong>Oh snap!</strong> <a href="#" class="alert-link">{!r} is not a number.</a>.
             </div>
             '''.format(request.form["number2"])
        try:
            original_amount = float(request.form["original_amount"])
        except:
            errors += '''
            <div class="alert alert-dismissible alert-danger">
                <button type="button" class="close" data-dismiss="alert">×</button>
                <strong>Oh snap!</strong> <a href="#" class="alert-link">{!r} is not a number.</a>.
             </div>
             '''.format(request.form["original_amount"])

        #if all of the fields are NOT empty
        if number1 is not None and number2 is not None and original_amount is not None:

            #if the year is out of bounds
            if ((number1 < 1800 or number1 > 2019) or (number2 < 1800 or number2 > 2019)):
                errors += '''
                <div class="alert alert-dismissible alert-danger">
                    <button type="button" class="close" data-dismiss="alert">×</button>
                    <strong>Oh snap!</strong> <a href="#" class="alert-link">Invalid range of dates, please try again.</a>
                 </div>
                 '''
                return render_template("dataEntry.html").format(errors=errors)

            #read and calculate data
            inflation_reader(dct)

            # for key in dct:
            #     result = calculate_pct_change(number1, int(key), dct)
            #     decimal_change = result / 100.0
            #     total_dollar = round((original_amount*decimal_change) + original_amount, 2)
            #     dct[key] = total_dollar

            #get the total percent change from one year to another
            result = calculate_pct_change(number1, number2, dct)

            #convert result to float
            decimal_change = result / 100.0

            #round to nearest tenths place in change
            total_dollar = round((original_amount*decimal_change) + original_amount, 2)

            #arrow import
            arrow = "../static/images/green_a.png"

            #if there is a decline, use a red arrow instead
            if (result < 0):
                arrow = "../static/images/red_arrow.png"

            #convert to strings to include ","
            total_dollar = '{:0,.2f}'.format(total_dollar)
            result = '{:0,.2f}'.format(result)

            for key in dct:
                dct[key] = calculate_dollar_change(key, number2, original_amount, dct)

            #data to send for creating chart
            chart_data = '''{
              labels: year_slice,
              series: [data_slice]
            }'''

            options = '''
            {
                showPoint: true
            }
            '''

            min_width = '''
                [['screen and (min-width: 640px)', { showPoint: false }]]
            '''

            #return successful result page
            return render_template("result.html").format(min_width = min_width, result=result, original_amount=original_amount, number1=number1, total_dollar=total_dollar, number2=number2, arrow=arrow, dct=dct, chart_data=chart_data, options=options)

    #return data entry page
    return render_template("dataEntry.html").format(errors=errors)

