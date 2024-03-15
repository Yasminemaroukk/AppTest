import http.client
from flask import Flask, request, render_template, jsonify
import os
from dotenv import load_dotenv

 
app = Flask(__name__)
load_dotenv()
APIKEY = os.getenv("APIKEY")
APIHOST = os.getenv("APIHOST")
 
def get_currency_exchange_rate(source_currency, target_currency, amount):
    conn = http.client.HTTPSConnection(APIHOST)
 
    headers = {
        'X-RapidAPI-Key': APIKEY,
        'X-RapidAPI-Host': APIHOST
    }
 
    querystring = f"/exchange?from={source_currency}&to={target_currency}&q={amount}"
 
    conn.request("GET", querystring, headers=headers)
 
    res = conn.getresponse()
    data = res.read()
 
    return data.decode("utf-8")
 
@app.route("/")
def index():
    return render_template("index.html")
 
@app.route("/convert", methods=["GET"])
def get_currency_value():
    source_currency = request.args.get("from", default="USD", type=str).upper()
    target_currency = request.args.get("to", default="USD", type=str).upper()
    amount = request.args.get("amount", default=1, type=float)
 
    exchange_rate_data = get_currency_exchange_rate(source_currency, target_currency, amount)
 
    return jsonify({"result": exchange_rate_data})
 
if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")
    debug_mode = env == "development"
    app.run(debug=debug_mode, host="0.0.0.0", port=5555)

