import logging
import requests
import pprint


# api docs used to find how to make the calls we want to make
# https://binance-docs.github.io/apidocs/#change-log

# The base endpoint for futures is: "https://fapi.binance.com"
# The REST baseurl for testnet is "https://testnet.binancefuture.com"
# The base endpoint for spot is: "https://api.binance.com"

# function to get a list of contracts/trading pairs from  binance futures
def get_available_contracts():
    # https://binance-docs.github.io/apidocs/futures/en/#exchange-information
    response_object = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")  # get request for the exchange info
    # print(response_object.status_code) # The 200 OK status code means that the request was successful
    # pprint.pprint(response_object.json()) # to print the full response - pretty print just makes the format nicer on the eye compared to print)

    # the binance api returns the response in a json format
    # JSON represents objects as name/value pairs, just like a Python dictionary so we just specify the correct key to access the value of the key

    contracts_list = []

    # for each dictionary ('contract' in the loop) in the list of dictionaries (response_object.json()['symbols']) add the "pair" to our contracts_list as the key "pair" contains the contract name
    for contract in response_object.json()['symbols']:
        contracts_list.append(contract['pair'])

    return contracts_list  # return our list

print(get_available_contracts())

