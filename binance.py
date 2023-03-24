import logging
import requests  # library to make requests using the http protocol
import pprint # pprint contains a “pretty printer” for producing aesthetically pleasing representations of your data structures

logger = logging.getLogger()

# api docs used to find how to make the calls we want to make
# https://binance-docs.github.io/apidocs/#change-log

# The base endpoint for futures is: "https://fapi.binance.com"
# The REST baseurl for futures testnet is "https://testnet.binancefuture.com"
# The base endpoint for spot is: "https://api.binance.com"


class BinanceClient:
    def __init__(self,testnet): # initialisation (basically a constructor) - testnet is a boolean indicating if were acting on the futures testnet or actual futures
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"

        logger.info("Binance client initialised")

        self.prices = dict() # empty dict on initialisation which will be used to store prices of different symbols/pairs

# we will use a make request method which can be called by the other functions , in this way the code becomes cleaner as we dont have to repeat these lines in each of the other functions
# method meaning the http methods GET or POST or DELETE, endpoint meaning the extra bit we need to add to the base url,
# params meaning any parameters as sometimes a api call might require parameters
    def make_request(self,method,endpoint,data):
        if method == 'GET':
           response = requests.get(self.base_url + endpoint, params=data)
        else:
            raise ValueError # we want to the program to crash if we we don't specify a GET method

        # if response code is 200 it means it was a success
        if response.status_code == 200:
            return response.json() # return the json response
        else:
            # we still put the the json response in the log error as it usually gives more info on the error
            logger.error(f"{response.status_code} response error code -> Error while making {method} request to the endpoint {endpoint}: {response.json()}")
            return None

# function to get a list of contracts/trading pairs from  binance futures
    def get_available_pairs(self):
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

    def get_contracts(self):

        exchange_info = self.make_request("GET", "/fapi/v1/exchangeInfo", None) # same as doing  exchange_info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")

        contracts = dict() # empty contracts dict

        if exchange_info is not None:  # if the make request method doesnt return None
            # for each dictionary ('contract_data' in the loop) in the list of dictionaries (exchange_info['symbols']) add the "pair" to our contracts_list as the key "pair" contains the contract name
            for contract_data in exchange_info['symbols']:  # for key-value pairs with the key 'symbols':
                contracts[contract_data['pair']] = contract_data  # eg. contracts["BLZUSDT"] = contract data (and so on for each pair (because of the for loop))

        return contracts

    def get_bid_ask(self, symbol):
        # From the API docs https://binance-docs.github.io/apidocs/futures/en/#symbol-order-book-ticker:
        # GET /fapi/v1/ticker/bookTicker -> Best price/qty on the order book for a symbol or symbols.
        # there is also a parameter of type string we can add (which is not mandatory) where we specify which symbol we want the price/qty for
        # If the symbol is not sent, bookTickers for all symbols will be returned
        # "https://testnet.binancefuture.com/fapi/v1/ticker/bookTicker?symbol=BTCUSDT"  # we add a  ? at the end and then specify parameters (we can use & for each additional other parameters we need to add)
        # however the get requests library and its get methods have a params keyword argument which lets us pass key/value pairs which will be added to the params parameters eg.
        data = dict()
        data['symbol'] = symbol  # so if we pass get_bid_ask("BTCUSDT") it will add the key value pair "symbol:BTCUSDT" to our dictionary called data
        # using the make_request method we defined
        order_book_data = self.make_request('GET', "/fapi/v1/ticker/bookTicker",data=data)  # same as doing request.get("https://testnet.binancefuture.com/fapi/v1/ticker/bookTicker?symbol=X") # where X is whatever symbol you specify in calling the get_bid_ask method

        if order_book_data is not None:  # i.e if request is returned successfully
            if symbol not in self.prices:  # if our symbol (eg.BTCUSDT) is not a key in the prices dictionary:
                # so were saying add the symbol key eg. prices["BTCUSDT"] and the values to a dict with the keys bid and ask: eg. {"bid":4.0000,"ask":4.00000}
                # if you look at the api docs we are interested in the bidPrice and askPrice keys
                # the values of those keys are given in string form eg. 'bidPrice':'12.60' so we use float to convert from string to the float values
                self.prices[symbol] = {'bid': float(order_book_data['bidPrice']),
                                       'ask': float(order_book_data['askPrice'])}
                # so eg. our dict would look something like this: {"BTCUSDT" : {"bid":4.0000,"ask":4.00000}}
            else:  # if the symbol is already a key then update the prices
                self.prices[symbol]['bid'] = float(order_book_data['bidPrice'])
                self.prices[symbol]['ask'] = float(order_book_data['askPrice'])

        return self.prices[symbol]  # return the data in the prices dict for the symbol we requested


    def get_candle_data(self, symbol, interval):
        # Read the API DOCS for candle stick data and below code will make sense:
        # https://binance-docs.github.io/apidocs/futures/en/#kline-candlestick-data
        data = dict()
        data['symbol'] = symbol  # for candle data requests the symbol is mandatory
        data['interval'] = interval  # interval meaning the timeframe , also mandatory
        data['limit'] = 1000  # not mandatory but we will increase it from the default value of 500 to 1000

        raw_candles = self.make_request("GET", "/fapi/v1/klines", data)

        candles = []

        if raw_candles is not None:  # if response is successful
            for c in raw_candles:  # if you look at the API docs the request returns lists within a list with each list representing a candlestick so c is a list
                # for each list/candlestick c we are appending the 1,2,3,4,5,6th elements to the list candles (we dont want all the other stuff eg. number of trades which is c[8])
                candles.append([c[0], float(c[1]), float(c[2]), float(c[3]), float(c[4]), float(c[5])])  # we have to use float as some of the elements which are numbers are given as strings

        return candles  # in essence we are essentially returning what raw candles gave us just with only the candlestick data we are concerned with


b = BinanceClient("https://testnet.binancefuture.com")
#pprint.pprint(b.get_contracts())
#print(b.get_available_pairs())
#print(b.get_bid_ask("BTCUSDT"))
#print(b.get_candle_data("ETHUSDT","1h"))

