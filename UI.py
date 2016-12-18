import tkinter as tk
from tkinter import *
from main import *

from colorizedInterface import *

FUNCS_HEADER = """\
from main import *
import main
import time
_Screen = screen
"""


def doIT(event=None):

   text =  entry.get("1.0", END)
   code = "".join([FUNCS_HEADER, text])
   print(code)
   exec(code, globals())

root = Tk()
entry = colorizedText(root)
entry.pack(side=LEFT, expand=1, fill=Y)
entry.bind("<F5>", doIT)
screen = Screen(root)
root.mainloop()
