import os
from flask import Flask, render_template, session, request
from flask import jsonify
import requests
import json
import hashlib
import hmac
import urllib2
import time

# Basic Script to generate a Coinbase payment button
# For more information on Coinbase's merchant services, see their homepage here: https://coinbase.com/merchants

coinbase_keys = {
    'secret_key': os.environ['API_KEY'],
    'publishable_key': os.environ['API_SECRET']
}

app = Flask(__name__)

#Authentication
def get_http(url, body=None):
  opener = urllib2.build_opener()
  nonce = int(time.time() * 1e6)
  message = str(nonce) + url + ('' if body is None else body)
  signature = hmac.new(os.environ['API_SECRET'], message, hashlib.sha256).hexdigest()
  opener.addheaders = [('ACCESS_KEY', os.environ['API_KEY']),
                       ('ACCESS_SIGNATURE', signature),
                       ('ACCESS_NONCE', nonce)]
  try:
    return opener.open(urllib2.Request(url, body))
  except urllib2.HTTPError as e:
    print e
    return e

#Minimum parameters for buttons API call
name="test"
price_string="1.23"
price_currency_iso="USD"

#stringified array for buttons API call
buttons_data = "button[name]=%s&button[price_string]=%s&button[price_currency_iso]=%s" % (name, price_string, price_currency_iso)

#POST to buttons API
buttons_response = get_http('https://coinbase.com/api/v1/buttons', body=buttons_data)
print buttons_response.read()

#for html page
@app.route('/')
def index():
    buttons_response = get_http('https://coinbase.com/api/v1/buttons', body=buttons_data)
    buttons = json.load(buttons_response)
    buttons_code = buttons['button']['code']
    print buttons_response.read()
    # print "Payment Page Link: https://coinbase.com/checkouts/" + buttons['button']['code']
    # print buttons_response['access_token']
    return render_template("index.html", code=buttons_code)




if __name__ == '__main__':
    app.run(debug=True, port=5002)
