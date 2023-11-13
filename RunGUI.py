# Import packages

from tkinter import *
from tkinter import messagebox, ttk
from nullifier import Querying
import os
import pandas as pd


# Define functions

class Interface:

    def __init__(self):
        self.func = Querying()
        self.no_urn_error_message ="***Please enter a valid URN number.***"
    

    def Run_GUI(self):
        # Initialise GUI

        GUI = Tk()

        GUI.geometry("400x200")
        GUI.title("data nullifier")

        # Set heading

        heading = Label(text = '''Enter the URN for the entry:''',
                         bg = "black", fg = "white", height = "3", width = "600")

        heading.pack()

        # Create number of days input

        self.URN_var = StringVar()

        URN_text = Label(text = "URN:")

        URN_entry = ttk.Entry(textvariable = self.URN_var)

        URN_text.place(x = "40", y = "65")

        URN_entry.place(x="140", y = "66")


        # Create and place button to generate data

        view_Tables = ttk.Button(text = "View Tables", command = lambda: Querying(self.URN_var.get()).show_tables())

        view_Tables.place(x= "4", y = "120", width = "392")

        # Create and place a button to transfer data from the data spreadsheet

        run_null = ttk.Button(text = "Nullify", command = lambda: self.nullifyandlog())

        run_null.place(x= "70", y = "150", width = "250")

        # Run GUI Loop

        GUI.mainloop()

    def confirm_FRM(self):
        conFRM = Toplevel()
        conFRM.geometry("400x200")
        conFRM.title("Enter the FRM Number for this ticket")

        FRM_var = StringVar()
        FRM_text = Label(conFRM, text = "FRM Number:")
        FRM_entry = ttk.Entry(conFRM, textvariable = FRM_var)
        confirm_bttn = ttk.Button(conFRM, text = "Log nullification", command = lambda: Querying(self.URN_var.get()).logit(FRM_var.get(), conFRM))

        FRM_text.place(x = "40", y = "65")
        FRM_entry.place(x="140", y = "66")
        confirm_bttn.place(x= "70", y = "150", width = "250")

        conFRM.mainloop()

    def nullifyandlog(self):
        Querying(self.URN_var.get()).run_nullifier()
        self.confirm_FRM()
               
        

Run_program = Interface()

Run_program.Run_GUI()
