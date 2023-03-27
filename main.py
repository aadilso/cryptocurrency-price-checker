import tkinter as tk  # Tkinter is the de facto way in Python to create Graphical User interfaces (GUIs) and is included in all standard Python Distributions
from tkinter import messagebox
from tkinter import ttk, font # tkk for combobox
from title_bar import *
import logging
from binance import BinanceClient

logger = logging.getLogger()  # instance of a logger object/ initialising logger object
logger.setLevel(logging.DEBUG)  # set min logging level to DEBUG meaning that debug and every level above will be logged

# for the messages to show up in the python terminal we need to create a stream handler object:
stream_handler = logging.StreamHandler()  # initialise stream handler object

# for the stream handler providing a format for the message
formatter = logging.Formatter('%(asctime)s - %(levelname)s :: %(message)s')  # creating a formatter object
stream_handler.setFormatter(formatter)  # set stream handler to our created format
stream_handler.setLevel(logging.INFO)  # set min logging level to INFO for the stream handler (debug messages wont show in the terminal as we don't want to overwhelm the terminal with messages)

# saving the logs to a file
file_handler = logging.FileHandler('info.log')  # creating file handler object and specifying the file will be used/created called info.log
file_handler.setFormatter(formatter)  # set the same format as the stream handler
file_handler.setLevel(logging.DEBUG)  # set min level to debug so even the debug messages will show in the file (along with the others - info,warning and error)

logger.addHandler(stream_handler)  # add the stream handler to our logger
logger.addHandler(file_handler)  # add the file handler to our logger


def show_data():
    entered_symbol = symbol_label_entry.get()

    if not entered_symbol: # if its empty
        messagebox.showerror("Error", "No symbol entered!")

    else:
        info_text.configure(state='normal')
        info_text.delete(0.0, tk.END)
        if entered_symbol not in binance.get_available_pairs():
            error = "The Symbol " + symbol_label_entry.get() + " is not a valid symbol! \nHere is a list of valid symbols: \n" + str(
                binance.get_available_pairs())
            info_text.insert(0.0, error)

        else:
            bid = binance.get_bid_ask(entered_symbol)['bid']
            ask = binance.get_bid_ask(entered_symbol)['ask']
            prices_info = entered_symbol + " latest bid price: $" + str(bid) + "\n" + entered_symbol + " latest ask price: $" + str(ask) + "\n"

            entered_interval = interval_combobox.get()  # get whats in the drop down/combobox
            last_ten_candles = binance.get_candle_data(entered_symbol, entered_interval)[-10:][::-1]  # get the last 10 candlestick data and reverse to gte most recent first
            candle_info = "\nSummary of the last 10 candlesticks for " + entered_symbol + " in the timeframe of " + entered_interval + "\n"
            count = 1
            for data_point in last_ten_candles:
                # the lists contain float so we need to convert to str to concatenate
                candle_info += "\n" + str(count) + entered_interval[1:] + " ago candlestick: " + entered_symbol + " opened with a price of $" + str(
                    data_point[1]) + " and closed at $" + str(
                    data_point[4]) + ". In this period it had a high of $" + str(
                    data_point[2]) + " and a low of $" + str(
                    data_point[3]) + " along with a volume of " + str(data_point[5]) + ".\n"
                count += 1

            info_text.insert(0.0, prices_info + candle_info)

        info_text.configure(state='disabled')

# ensuring only if the the program is called from main.py then the code inside will run (if we import the class to another class and run it the code inside the if statement will not run
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do for more in depth explanation


if __name__ == '__main__':
    binance = BinanceClient(True)
    binance_symbols = binance.get_available_pairs()
    root = tk.Tk()  # creating a Tk object - this represent the main window of the application

    # list of all available fonts in tkinter
    # for font in font.families():
    #     print(font)

    dark_title_bar(root)
    root.title("Cryptocurrency Price Checker")
    # root.geometry("800x800")  # setting size
    background_colour = "Black"
    foreground_colour = "Yellow"
    # defining fonts
    my_font = ("Cascadia Code Light", 14, "normal")
    my_title_font = ("Cascadia Code Light", 20, "bold")
    root.config(bg=background_colour) # ensure empty spaces are not shown as white

    # Title Label
    title_label = tk.Label(root, text="Cryptocurrency Price Checker", bg=background_colour,fg=foreground_colour, font=my_title_font)
    # Creating main form to enter symbol and time frames:
    symbol = tk.Label(root, text="Enter the symbol for which you would like information for:", bg=background_colour,fg=foreground_colour,font=my_font)
    # creating entry box for symbol:
    symbol_label_entry = tk.Entry(root, width=30,font=my_font, justify=tk.CENTER,bg=background_colour,fg=foreground_colour)
    interval = tk.Label(root, text="Select the candle stick interval for the symbol you entered:", bg=background_colour, fg=foreground_colour, font=my_font)
    # drop down for intervals using combobox

    # styling -> https://stackoverflow.com/questions/27912250/how-to-set-the-background-color-of-a-ttk-combobox
    combostyle = ttk.Style()
    combostyle.theme_create('combostyle', parent='alt',
                            settings={'TCombobox':
                                          {'configure':
                                               {'selectbackground': background_colour,
                                                'fieldbackground': background_colour,
                                                'background': foreground_colour
                                                }}}
                            )
    combostyle.theme_use('combostyle')

    intervals = ["1m", "1h", "6h", "12h", "1d", "1w"]
    interval_combobox = ttk.Combobox(root,width=40,font=my_font, value=intervals, justify="center",foreground=foreground_colour,background=background_colour,state="readonly")
    # for changing the colours of the dropdown of the numbers: https://stackoverflow.com/questions/62613030/how-to-change-the-color-of-the-dropdown-text-color-of-ttk-combobox-widget
    interval_combobox.tk.eval('[ttk::combobox::PopdownWindow %s].f.l configure -background black -foreground yellow' % interval_combobox)
    interval_combobox.current(1) # default option is index 1 (1h)
    # Get price info button
    get_info_button = tk.Button(root, text="Get Price Information", bg=background_colour,fg=foreground_colour,font=my_font,command=show_data)
    info_text = tk.Text(root, state='disabled', width=90, height=32, bg=background_colour,fg=foreground_colour,wrap=tk.WORD,padx=15,font=my_font,bd=0) # wrap = word so that we dont have half of a word on 1 line and the other half on the next

    title_label.pack(pady=(5,25))
    symbol.pack()
    symbol_label_entry.pack(pady=(0,10))
    interval.pack()
    interval_combobox.pack(pady=(0,15))
    get_info_button.pack(pady=(15,30))
    info_text.pack()

    #get_info_button.place(relx=0.5, rely=0.25,anchor='center')  # https://stackoverflow.com/questions/31128780/tkinter-how-to-make-a-button-center-itself

    #get_info_text.place(relx=0.5, rely=0.65, anchor='center')

    # print(binance.get_bid_ask("BTCUSDT"))
    # print(binance.get_bid_ask("ETHUSDT"))
    # print(binance.prices)  # our prices dict from the binance class
    # btc candle data on the 1 hour time frame (we set limit to 100 in the methods code so it will give us the last 100 candles in the 1h time frame) - note it gives oldest first to newest (first the 1000 candle then lastly the newest most recent candles)
    # print(binance.get_candle_data("BTCUSDT", "1h")) # 1m 1h 6h 12h 1d 1w

    root.mainloop()  # Mainloop in Python Tkinter is an infinite loop of the application window which runs forever (until we close) so that we can see the still screen.
