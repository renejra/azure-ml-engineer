import urllib.request
import json
import os
import ssl

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

# Request data goes here
# data = {
# }

data = {
        "data":
            [
              {
                "age": 17,
                "campaign": 1,
                "cons.conf.idx": -46.2,
                "cons.price.idx": 92.893,
                "contact": "cellular",
                "day_of_week": "mon",
                "default": "no",
                "duration": 971,
                "education": "university.degree",
                "emp.var.rate": -1.8,
                "euribor3m": 1.299,
                "housing": "yes",
                "job": "blue-collar",
                "loan": "yes",
                "marital": "married",
                "month": "may",
                "nr.employed": 5099.1,
                "pdays": 999,
                "poutcome": "failure",
                "previous": 1
              }
          ],
        "method": "predict"
        }

body = str.encode(json.dumps(data))

url = 'http://c881a363-28fd-426b-ab8d-96173fafd1d4.southcentralus.azurecontainer.io/score'
api_key = 'LYR4HEiLcHGLeKnz2Nqzv0VMZj0i9hjQ' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))