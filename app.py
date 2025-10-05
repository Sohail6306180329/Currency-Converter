from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Currency conversion logic using ExchangeRate-API
def convert_currency(from_currency, to_currency, amount):
    url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Error: Unable to fetch exchange rate"
    
    data = response.json()
    rate = data["rates"].get(to_currency)

    if rate:
        return round(float(amount) * rate, 2)
    else:
        return "Conversion failed"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        from_currency = request.form['from_currency']
        to_currency = request.form['to_currency']
        amount = request.form['amount']
        
        result = convert_currency(from_currency, to_currency, amount)

    currencies = ["USD", "INR", "EUR", "GBP", "JPY", "CAD", "CNY", "CHF"]
    return render_template("index.html", currencies=currencies, result=result)

if __name__ == '__main__':
    app.run(debug=True)