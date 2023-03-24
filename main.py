import tkinter as tk  # Tkinter is the de facto way in Python to create Graphical User interfaces (GUIs) and is included in all standard Python Distributions
import logging
from binance import BinanceClient

logger = logging.getLogger()  # instance of a logger object/ initialising logger object
logger.setLevel(logging.DEBUG)  # set min logging level to DEBUG meaning that debug and every level above will be logged

# for the messages to show up in the python terminal we need to create a stream handler object:
stream_handler = logging.StreamHandler() # initialise stream handler object

# for the stream handler providing a format for the message
formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s') # creating a formatter object
stream_handler.setFormatter(formatter) # set stream handler to our created format
stream_handler.setLevel(logging.INFO) # set min logging level to INFO for the stream handler (debug messages wont show in the terminal as we don't want to overwhelm the terminal with messages)

# saving the logs to a file
file_handler = logging.FileHandler('info.log') # creating file handler object and specifying the file will be used/created called info.log
file_handler.setFormatter(formatter) # set the same format as the stream handler
file_handler.setLevel(logging.DEBUG) # set min level to debug so even the debug messages will show in the file (along with the others - info,warning and error)

logger.addHandler(stream_handler) # add the stream handler to our logger
logger.addHandler(file_handler) # add the file handler to our logger

def show_data():
    get_info_text.configure(state='normal')
    get_info_text.delete(0.0, tk.END)
    symbol = symbol_label_entry.get()
    if symbol not in binance.get_available_pairs():
        error = "The Symbol " + symbol_label_entry.get() + " is not a valid symbol!. \n Here is a list of valid symbols: \n" + str(binance.get_available_pairs())
        get_info_text.insert(0.0,error)
        get_info_text.configure(state='disabled')
    else: # it is a valid symbol

        header = "Heres the latest price info for " + symbol_label_entry.get() + ":\n"
        prices_info = str(binance.get_bid_ask(symbol))

        interval = clicked.get() # get whats in the drop down
        last_ten = binance.get_candle_data(symbol,interval)[-10:][::-1] # get the last 10 candlestick data and reverse to gte most recent first
        candle_info = "\nSummary of the last 10 candlesticks for the timeframe of " + interval + " (starting with the most recent)\n"
        for data_point in last_ten:
            # the lists contain float so we need to convert to str to concatenate
            candle_info += "\n" + symbol + " opened with a price of $" + str(data_point[1]) + " and closed at $" + str(data_point[4]) + ".In this period it had a high of $" + str(data_point[2]) + " and a low of $" + str(data_point[3]) + " along with a volume of " + str(data_point[5]) + ".\n"

        #candles_info = " Here's the candle stick data for the last " + clicked.get() + ": "  + str(candle_date[-1])
        get_info_text.insert(0.0,header + prices_info + candle_info)
        get_info_text.configure(state='disabled')

# ensuring only if the the program is called from main.py then the code inside will run (if we import the class to another class and run it the code inside the if statement will not run
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do for more in depth explanation
if __name__ == '__main__':
    binance = BinanceClient(True)
    binance_contracts = binance.get_available_pairs()
    root = tk.Tk()  # creating a Tk object - this represent the main window of the application
    root.title("Cryptocurrency Price Checker")
    root.geometry("800x800") # setting size
    background_colour = "AntiqueWhite2"
    root.config(bg=background_colour) # without this the empty sections will still be white
    # if you run at this point the program will not show anything hence the below code

    my_font = ("Calibri", 14, "normal")  # defining a font using a tuple
    my_title_font = ("Arial", 20, "bold")  # defining a title font using a tuple

    title_label = tk.Label(root,text="Cryptocurrency Price Checker",bg=background_colour,font=my_title_font)
    title_label.grid(row=0,column=0,pady=(30,20)) # https://stackoverflow.com/questions/4174575/adding-padding-to-a-tkinter-widget-only-on-one-side

    # Creating main form to enter symbol and time frames etc
    symbol = tk.Label(root,text="Enter the symbol for which you would like information for",bg=background_colour,font=my_font).grid(row=1,column=0,sticky="W",padx=10)
    interval = tk.Label(root,text="Select the candle stick interval for the symbol you entered",bg=background_colour,font=my_font).grid(row=2,column=0,sticky="W",padx=10)

    # creating entry box for symbol:
    symbol_label_entry = tk.Entry(root,width=30)
    symbol_label_entry.grid(row=1,column=1)

    # drop down for intervals
    clicked = tk.StringVar()
    clicked.set("1h")
    interval_label_drop = tk.OptionMenu(root,clicked,"1m","1h","6h","12h","1d","1w")
    interval_label_drop.config(width=24)
    interval_label_drop.grid(row=2, column=1)

    # Get price info button:
    get_info_button = tk.Button(root,text="Get Price Information",command=show_data)
    get_info_button.place(relx=0.5, rely=0.25, anchor='center') # https://stackoverflow.com/questions/31128780/tkinter-how-to-make-a-button-center-itself


    get_info_text = tk.Text(root,state='disabled',width=95,height = 35,bg = background_colour)
    get_info_text.place(relx=0.5, rely=0.65, anchor='center')


    # row_no = 0  # initialising to 0 means the first widget will be placed on the first row
    # column_no = 0  # initialising to 0 means the first widget will be placed on the first column
    # we have to do this before the root.mainloop() as that code keeps infinitely showing the gui so of course the gui needs to be done before that code is called



    # for contract in binance_contracts:
    #     label_widget = tk.Label(root, text=contract,
    #                             borderwidth=1,
    #                             relief=tk.SOLID, # there is also tk.GROOVE AND RIDGE so maybe try those if you want a different outline
    #                             width=10, # also width = 10 ensures each column is of length 10 and some are not different lengths
    #                             bg='gray12',  # background colour
    #                             fg='SteelBlue1',  # foreground colour
    #                             font=my_font)  # the font
    #     # label_widget.pack(side=tk.TOP) - using a pack layout is 1 of the 2 ways to display the data but because we have a lot of things to display it it not the most appropriate, grid is more appropriate
    #     label_widget.grid(row=row_no,column=column_no)
    #     # if we reach the 7th row (since 0 counts as 1st row):
    #     if row_no == 6:
    #         column_no += 1  # start adding the widgets to the next column
    #         row_no = 0  # reset the row to 0
    #     else:  # if not just keep adding on the next row:
    #         row_no += 1  # each time we increase row no by 1 as we want each symbol on a new row

    # get bid ask methods to get eth and btc bid ask prices
    #print(binance.get_bid_ask("BTCUSDT"))
   # print(binance.get_bid_ask("ETHUSDT"))
   # print(binance.prices)  # our prices dict from the binance futures class

    # btc candle data on the 1 hour time frame (we set limit to 1000 in the methods code so it will give us the last 1000 candles in the 1h time frame) - note it gives oldest first to newest (first the 1000 candle then lastly the newest most recent candles)
    #print(binance.get_candle_data("BTCUSDT", "1h")) # 1m 1h 6h 12h 1d 1w

    # text = tk.Text(root, width=80, height=15)
    # text.pack()
    # for contract in binance_contracts:
    #     text.insert(tk.END, contract + '\n' )

    root.mainloop()  # Mainloop in Python Tkinter is an infinite loop of the application window which runs forever (until we close) so that we can see the still screen.




