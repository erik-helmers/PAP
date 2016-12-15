
import tkinter as tk
from tkinter import *
from main import *
import main
FUNCS_NAME = main.__funcs_screen+main.__funcs_pen
VAR_CHAR = [(97, 122), (65, 90), (95, 95), (49, 57)]
_TEST_VAR_CHAR = lambda s: True in map((lambda x: x[0]<=ord(s)<=x[1]), VAR_CHAR)


def _get_word(s, pos): #Prend une pos en "%s.%s"
    print(s, pos)
    posFirst, pos = map(int, pos.split("."))
    output = [s[pos]]
    iFin=pos+1
    while 0<=iFin<len(s) and  _TEST_VAR_CHAR (s[iFin]):
        output.append(s[iFin])
        iFin+=1
    iDeb=pos-1
    while 0<=iDeb<len(s) and  _TEST_VAR_CHAR (s[iDeb]):
        output.insert(0, s[iDeb])
        iDeb-=1
    return "".join(output), "%s.%s" % (posFirst, iDeb+1), "%s.%s" % (posFirst, iFin)



class CustomText(tk.Text):
    '''A text widget with a new method, highlight_pattern()

    example:

    text = CustomText()
    text.tag_configure("red", foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")

    The highlight_pattern method is a simplified python
    version of the tcl code at http://wiki.tcl.tk/3246
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.rooot = args[0]
    def highlight_pattern(self, s, tag, start="1.0", end="end",
                          regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular
        expression according to Tcl's regular expression syntax.
        '''
        print("pos :", text.index("insert"))
        if s == "forward" : self.rooot.after(100, lambda :self.tag_add(tag, start, end))
        print("colored it with tag_add")
        # start = self.index(start)
        # end = self.index(end)
        # self.mark_set("matchStart", start)
        # self.mark_set("matchEnd", start)
        # self.mark_set("searchLimit", end)
        # print(self.get(start, end))
        # count = tk.IntVar()
        # while True:
        #     index = self.search(pattern, "matchEnd","searchLimit",
        #                         count=count, regexp=regexp)
        #     if index == "": break
        #     if count.get() == 0: break # degenerate pattern which matches zero-length strings
        #     self.mark_set("matchStart", index)
        #     self.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
        #     self.tag_add(tag, "matchStart", "matchEnd")

        
        ranges = text.tag_ranges("red")
        for i in range(0, len(ranges), 2):
            start = ranges[i]
            stop = ranges[i+1]
            if s != "forward":
                self.tag_remove("red", start, stop)
                print("wow '%s' != 'forward'" %(s))
def test(event):
    tex = list(text.get
                ("insert linestart", "insert lineend"))
    #print("Pos :",text.index("insert"))
    
    if event.keysym=="BackSpace":
        print(tex.pop(int(text.index("insert").split(".")[1])-1))
    if event.keysym=="Delete":
        print(tex.pop(int(text.index("insert").split(".")[1])))
    else: tex.insert(int(text.index("insert").split(".")[1]), event.char)
    word = _get_word("".join(tex), text.index("insert"))
    print ("Word :", word)
    text.highlight_pattern(word[0], "red", word[1], word[2])
    
root = Tk()

text = CustomText(root)
text.tag_configure("red", foreground="#ff0000")
text.bind("<Key>",test)
root.after(1000, lambda : print("a"))
text.pack()
root.update()
