#SomeSandBox

import re

from  main import ALL_FUNCS_NAME

from tkinter import Text, BOTH
from tkinter import *


_built_in_funcs_name = {2: ['id'],
                        3: ['abs', 'all', 'any', 'bin', 'chr', 'cmp', 'dir',
                            'hex', 'int', 'len', 'map', 'max', 'min', 'oct', 'ord',
                            'pow', 'set', 'str', 'sum', 'zip'],
                        4: ['bool', 'dict',
                            'eval', 'file', 'hash', 'help', 'iter', 'list', 'long', 'next',
                            'open', 'repr', 'type', 'vars'],
                        5: ['print','float', 'input', 'print', 'range', 'round', 'slice',
                            'super', 'tuple'],
                        6: ['divmod', 'filter', 'format','locals', 'object',
                            'reduce', 'reload', 'sorted', 'unichr', 'xrange'],
                        7: ['compile', 'complex', 'delattr', 'getattr',
                            'globals', 'hasattr', 'setattr', 'unicode'],
                        8: ['callable', 'execfile', 'property', 'reversed'],
                        9: ['bytearray', 'enumerate', 'frozenset', 'raw_input'],
                        10: ['__import__', 'basestring', 'isinstance',
                             'issubclass', 'memoryview'],
                        11: ['classmethod'], 12: ['staticmethod']}

_key_words_name = {2: ['as', 'or', 'if', 'in', 'is'],
                   3: ['and', 'del', 'not', 'def', 'for', 'try'],
                   4: ['from','True','None', 'elif', 'with', 'else', 'pass', 'exec'],
                   5: ['while', 'False', 'yield', 'break', 'class', 'raise'],
                   6: ['global', 'assert', 'except', 'import', 'return', 'lambda'],
                   7: ['finally'], 8: ['continue']}


goodChar = lambda x: x.isalpha() or x.isdigit()
breakChar = lambda x: x in [",", ".", "'", "(", ")", ";", " ",
                            ":", '"', "-", "&", "=", "%",
                            "*", "/", "+"]


def _get_int_index(index):
    return list(map(int, index.split(".")))

def _get_string_index(x, y):
    return "%s.%s" %(x, y)

def _get_word(line, pos):

    posString = isinstance(pos, str) or outString
    if posString:
        pos= _get_int_index(pos)

    if pos[1]>0: pos[1] -= 1 # 1.1 -> index 0
    if pos[1]<0 or pos[1]>=len(line): return "not_found"

    output = line[pos[1]]



    posDeb, posFin = pos[1]-1, pos[1]+1
    while 0<=posDeb<len(line) and goodChar(line[posDeb]): posDeb-=1
    while 0<=posFin<len(line) and goodChar(line[posFin]): posFin+=1

    word = line[posDeb+1:posFin]
    try:
        if not goodChar(word[0]):
            word = word[1::1]
            posDeb += 1
        if not goodChar(word[-1]):
            word = word[0:-1]
            posFin -= 1
    except IndexError: pass
    for ix, x in enumerate(word):
        if not goodChar(x):
            return ((word[0:ix], _get_string_index(pos[0], posDeb+1),
                     _get_string_index(pos[0], posDeb+ix+1)),
                    (word[ix+1::1], _get_string_index(pos[0], ix+1),
                     _get_string_index(pos[0], posFin)))
        
    if posString: return((word, _get_string_index(pos[0], posDeb+1),
                          _get_string_index(pos[0], posFin)),)

    else: return((word, [pos[0], posDeb+1], [pos[1], posFin]),)



class __ModifiedMixin:
    '''
    Class to allow a Tkinter Text widget to notice when it's modified.

    To use this mixin, subclass from Tkinter.Text and the mixin, then write
    an __init__() method for the new class that calls _init().

    Then override the beenModified() method to implement the behavior that
    you want to happen when the Text is modified.
    '''

    def _init(self):
        '''
        Prepare the Text for modification notification.
        '''

        # Clear the modified flag, as a side effect this also gives the
        # instance a _resetting_modified_flag attribute.
        self.clearModifiedFlag()

        # Bind the <<Modified>> virtual event to the internal callback.
        self.bind_all('<<Modified>>', self._beenModified)

    def _beenModified(self, event=None):
        '''
        Call the user callback. Clear the Tk 'modified' variable of the Text.
        '''
        # If this is being called recursively as a result of the call to
        # clearModifiedFlag() immediately below, then we do nothing.
        if self._resetting_modified_flag: return

        # Clear the Tk 'modified' variable.
        self.clearModifiedFlag()

        # Call the user-defined callback.
        self.beenModified(event)

    def beenModified(self, event=None):
        '''
        Override this method in your class to do what you want when the Text
        is modified.

        '''
        pass

    def clearModifiedFlag(self):
        '''
        Clear the Tk 'modified' variable of the Text.

        Uses the _resetting_modified_flag attribute as a sentinel against
        triggering _beenModified() recursively when setting 'modified' to 0.
        '''

        # Set the sentinel.
        self._resetting_modified_flag = True

        try:

            # Set 'modified' to 0.  This will also trigger the <<Modified>>
            # virtual event which is why we need the sentinel.
            self.tk.call(self._w, 'edit', 'modified', 0)

        finally:
            # Clean the sentinel.
            self._resetting_modified_flag = False
    



class colorizedText(__ModifiedMixin, Text):
    '''
    Subclass both ModifiedMixin and Tkinter.Text.
    '''

    def index_insert(self): return _get_int_index(self.index("insert"))

    def __init__(self, *a, **b):

        try: self.master = a[0]
        except IndexError: raise TypeError("Must be a tk for first args")
        # Create self as a Text.
        Text.__init__(self, *a, **b)
        self.textlen = 0

        # Initialize the ModifiedMixin.
        self._init()

        #Initialize the tags
        self.tag_config("pap_funcs_name", foreground="#ff0000", fg="gray75",

                       wrap=NONE)
        self.tag_config("built_in_funcs_name", foreground="blue",
                        wrap=NONE)
        self.tag_config("key_words_name", foreground = "green",
                        wrap=NONE)
    def beenModified(self, event=None):
        '''
        Override this method do do work when the Text is modified.
        '''
        words  =  _get_word(self.get("insert linestart", "insert lineend"),
                                  self.index("insert"))
        textlen = len(self.get("1.0", END))
        if not  -2 <=textlen-self.textlen <= 2:
            self.textlen = textlen
            return self.colorize_all()

        self.textlen = textlen
        if words == "not_found" : return 

        self.colorize(words)

    def colorize_all(self):
        text = self.get("1.0", END)
        words = []

        posDeb = [1, 0]
        posFin = [1, 0]
        word = []

        for letter in text:

            if goodChar(letter):
                posFin[1] += 1
                word.append(letter)
            elif letter == "\n":
                if word != []:
                    words.append(("".join(word), [*posDeb], [*posFin]))
                    word = []
                posDeb = [posDeb[0]+1, 0]
                posFin = [posDeb[0], 0]
            else:
                if word != []:
                    words.append(("".join(word), [*posDeb], [*posFin]),)
                    word = []
                posDeb = [posFin[0], posFin[1]+1]
                posFin = posDeb.copy()
        self.colorize(words)
        return words


    def colorize(self, words):
        """Take a list of tuple with a word and his start
    and end index in the text widget, and colorize it with
    the parameters in the funcs define by the funcs:
    i.e.:keywords in blue, pap funcs in red and built-in in bue"""

        for word, deb, fin in words :
            if isinstance(deb, (list, tuple)):
                deb, fin = _get_string_index(*deb), _get_string_index(*fin)
            self.tag_remove("key_words_name", deb, fin)
            self.tag_remove("built_in_funcs_name", deb, fin)
            
            if word in ALL_FUNCS_NAME:
                self.tag_add("pap_funcs_name", deb, fin)
                self.tag_remove("built_in_funcs_name", deb, fin)
                self.tag_remove("key_words_name", deb, fin) 
                self.update()
            else:
                self.tag_remove("pap_funcs_name",deb, fin)

            if len(word) in _built_in_funcs_name.keys():
                if word in _built_in_funcs_name[len(word)]:
                    self.tag_add("built_in_funcs_name", deb, fin)
                    self.update()
            
            if len(word) in _key_words_name.keys():
                if word in _key_words_name[len(word)]:
                    self.tag_add("key_words_name", deb, fin)
                    self.update()


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError ("cannot use pack with this widget")
    def place(self, **kw):
        raise TclError("cannot use place with this widget")



class PAPEditor(Frame):

    def __init__(self, *args, **kwargs):

        
        #Init the Frame class
        Frame.__init__(self, *args, **kwargs)

        vscrollbar = AutoScrollbar(self)
        vscrollbar.grid(row=0, column=1, sticky=N+S)
        hscrollbar = AutoScrollbar(self, orient=HORIZONTAL)
        hscrollbar.grid(row=1, column=0, sticky=E+W)

        self.entry = colorizedText(self,
                        yscrollcommand=vscrollbar.set,
                        xscrollcommand=hscrollbar.set)
        self.entry.grid(row=0, column=0, sticky=N+S+E+W)

        vscrollbar.config(command=self.entry.yview)
        hscrollbar.config(command=self.entry.xview)

        # make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def focus_set(self):
        self.entry.focus_set()

if __name__=="__main__":
    root = Tk()
    Label(root, text="EFIEAJAIE").grid(column = 1, row = 0)
    
    PAPEditor(root).grid(row = 0, column = 0, sticky = N+S)
    
    root.mainloop()
