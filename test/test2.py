from tkinter import *
import tkinter.filedialog as tkfd

def save():
    savenm = tkfd.asksaveasfile()
    f = open(savenm.name,"w")
    # then put what to do with the opened file
def openf():
    opennm = tkfd.askopenfile()
    f = open(savenm.name,"r")
    # then put what to do with the opened file
print(tkfd.asksaveasfile())
print(tkfd.askopenfile())
