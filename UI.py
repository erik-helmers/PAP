import sys
import main

from main import *
from cons import *

if sys.version_info[0]==2:
    import Tkinter as TK
else :
    import tkinter as TK

#Fenetre avec coté gauche interpréteur et a droite output
# => IDLE features


INTRO_CODE = """\
from main import *
import main
main._Screen = self.output
"""

FUNCS_NAME = main.__funcs_screen+main.__funcs_pen
VAR_CHAR = [(97, 122), (65, 90), (95, 95), (49, 57)]

class ShellLike:

    def __init__(self, root=None):
        if not root: root = Tk()
        self.tk = root

        


        

class App:

    def __init__(self):

        self.tk = Tk()

        alert = lambda: None
        self.menubar = menubar = Menu(self.tk)

        menu1 = Menu(menubar, tearoff=0)
        menu1.add_command(label="Créer", command=alert)
        menu1.add_command(label="Editer", command=alert)
        menu1.add_separator()
        menu1.add_command(label="Quitter", command=sys.exit)
        menubar.add_cascade(label="Fichier", menu=menu1)

        menu2 = Menu(menubar, tearoff=0)
        menu2.add_command(label="Couper", command=alert)
        menu2.add_command(label="Copier", command=alert)
        menu2.add_command(label="Coller", command=alert)
        menubar.add_cascade(label="Editer", menu=menu2)

        menu3 = Menu(menubar, tearoff=0)
        menu3.add_command(label="A propos", command=alert)
        menubar.add_cascade(label="Aide", menu=menu3)

        self.tk.config(menu=menubar)

        self.entry = Text(self.tk)
        self.entry.pack(side=LEFT, fill=Y)
        self.entry.config(takefocus=True)
        self.entry.focus_set()

        self.entry.bind("<Key>", self.__change__)
        self.entry.bind("<F5>", self.__exct__)

        self.sentence = []
        self.text = []

        
        self.output = Screen(self.tk)

            
    def __change__(self, event=None):
        self.text = (self.entry.get("1.0", END)+event.char)
        print(self.text)

        
        
    def __exct__(self, event=None):
        code = self.entry.get("1.0", END)
        print(code)
        code = "\n".join([INTRO_CODE, code, ""])
        exec(code)

a = App()
