#SomeSandBox

import re

from  main import ALL_FUNCS_NAME

from tkinter import Text, BOTH
from tkinter import *


goodChar = lambda x: x.isalpha() or x.isdigit()
breakChar = lambda x: x in [",", ".", "'", "(", ")", ";", " "]

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

    if breakChar(word[0]):
        word = word[1::1]
        posDeb += 1
    if breakChar(word[-1]):
        word = word[0:-1]
        posFin -= 1

    for ix, x in enumerate(word):
        if not goodChar(x):
            return ((word[0:ix], _get_string_index(pos[0], posDeb+1),
                     _get_string_index(pos[0], posDeb+ix+1)),
                    (word[ix+1::1], _get_string_index(pos[0], ix+1),
                     _get_string_index(pos[0], posFin)))
        
    if posString: return((word, _get_string_index(pos[0], posDeb+1),
                          _get_string_index(pos[0], posFin)),)
    else: return((word, [pos[0], posDeb+1], [pos[1], posFin]),)

class ModifiedMixin:
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
    



class T(ModifiedMixin, Text):
    '''
    Subclass both ModifiedMixin and Tkinter.Text.
    '''

    def __init__(self, *a, **b):

        # Create self as a Text.
        Text.__init__(self, *a, **b)

        # Initialize the ModifiedMixin.
        self._init()

        #Initialize the tags
        self.tag_config("pap_funcs_name", foreground="#ff0000", fg="gray75")
        
    def beenModified(self, event=None):
        '''
        Override this method do do work when the Text is modified.
        '''
        words  =  _get_word(self.get("insert linestart", "insert lineend"),
                                  self.index("insert"))

        if words == "not_found" : return 

        for word, deb, fin in words:
            if word in ALL_FUNCS_NAME:
                self.tag_add("pap_funcs_name", deb, fin)
                self.update()
            else:
                self.tag_remove("pap_funcs_name",deb, fin)
t = T()
t.pack(expand=1, fill=BOTH)
t.mainloop()
