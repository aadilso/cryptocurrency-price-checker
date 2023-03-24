import tkinter as tk  # Tkinter is the de facto way in Python to create Graphical User interfaces (GUIs) and is included in all standard Python Distributions
from binance import * # importing write log method from binance class

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

# configuring the different messages of the logger
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.warning('This is a warning message')
logger.error('This is an error message')


# ensuring only if the the program is called from main.py then the code inside will run (if we import the class to another class and run it the code inside the if statement will not run
# https://stackoverflow.com/questions/419163/what-does-if-name-main-do for more in depth explanation
if __name__ == '__main__':
    root = tk.Tk()  # creating a Tk object - this represent the main window of the application
    # if you run at this point the program will not show anything hence the below code
    root.mainloop()  # Mainloop in Python Tkinter is an infinite loop of the application window which runs forever (until we close) so that we can see the still screen.