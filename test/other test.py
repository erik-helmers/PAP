import main
from main import *

root = Tk()
screen = Screen(root)
entry = Label(root, text= "HELLO WORLD")
entry.pack(side = TOP, expand = 1, fill=Y)
#main._Screen = screen
forward(10)
root.mainloop()
