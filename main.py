#!/usr/bin/python3


from cons import *
import sys, time, inspect, math
import random

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *


__funcs_screen = ["background", "getScreen", "update", "c_empty", "c_undo"]
__funcs_pen = ["cercle", "forward", "rotate", "left", "right", "undo",
               "is_empty", "setColor", "dirty_circle", "logo"]


ALL_FUNCS_NAME = __funcs_screen + __funcs_pen + ["init", "reset"]

class PAP_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr("Une erreur est survenue:",self.value)

class Terminated(Exception):
    def __init__(self): pass
    def __str__(self):
        print("========================================================\n\
\
\
La fenêtre a été fermée. Les commandes sont désactivées.\
\n\
========================================================\
")
        return ""



class Screen(Frame):
    """
    Screen does the display gestion

    It contains a canvas with added functionnalities.
    Canvas origin (0,0) is always in the middle of screen.
    Has an auto-binded button (F11) to switch to fullscreen.

     """

    __name__ = "Screen"

    __count__ = 0

    def __init__(self, *args, **kwargs):

        """
        Create a new screen instance

        KEYWORDS :
           - when no one are given : auto create a Tk() instance
           - else : extends Frame
        """

        # ============================================= INITIALISATION ========================================

        if args==():
            self.master = Tk();
            self.isFrame = False #Permet l'importation de la fenetre en tant que frame
            self.master.title("PAP screen id %s" %(random.randint(0, 1000)))
        else:                                               #ou en tant que standalone.
            self.isFrame = True
            Frame.__init__(self, *args, **kwargs)
            self.frame = self
            self.master = args[0]
            print("hello", self.frame)

        # =============================================== BINDING =============================================

        # Ce Bind est primordial afin de pouvoir centrer continuelement l'image
        # et ne pas étendre le canvas vers un côté précis.

        self.master.bind("<Configure>", self.__reconfig__)


        # =============================================== CANVAS ==============================================

        self.canvas = Canvas(self.getRoot(), bg=CANVAS_BACKGROUND)
        self.canvas.grid(sticky = W+E+N+S)

        self.getRoot().grid_rowconfigure(0, weight=1)
        self.getRoot().grid_columnconfigure(0, weight=1)

        # =============================================== FULLSCREEN ==============================================

        self.is_fullscreen = False
        self.master.bind("<F11>", self.toogle_fullscreen)
        # ================================================ ID =================================================

        Screen.__count__ += 1
        self.id = "Screen_"+str(Screen.__count__)


    def toogle_fullscreen(self, force=None, event=None):
        """
        Change fullscreen mode

        KEYWORDS:
          - force(boolean): if is None, switch fullscreen,
            else set fullscreen to force
        """
        if force==None: force = not self.is_fullscreen
        self.is_fullscreen = force
        self.master.wm_attributes("-fullscreen", self.is_fullscreen)
    def getRoot(self):
        """
        Return root Tk() instance or Frame. 

        (if created as frame, return frame, else return master)
        """
        if self.isFrame: return self.frame
        else: return self.master

    def reset(self):
        """
        Blank the canvas
        """
        self.canvas.delete(ALL)
        self.update()

    def __reconfig__(self, event):
        """
        On screen change set the 0,0 point to screen middle
        """
        x, y = event.width//2, event.height//2
        self.canvas.config(scrollregion=(-x, -y, x, y))

    def background(self, color):
        """
        Takes a color and set background color to it
        """
        if isinstance(color, (int, int, int)):
            pass
        else: self.canvas.config(background=color)

    def getScreen(self):
        """
        hack function
        """
        return self

    def update(self):
        """
        update the canvas
        """
        self.canvas.update()

    def c_empty(self):
        """
        return True if canvas is empty
        """
        return self.canvas.find_all()==()
    def c_undo(self):
        """
        remove the last item drawed on canvas
        """
        try:
            self.canvas.delete(self.canvas.find_all()[-1])
            self.update()
            return True
        except: return False

    def __repr__(self):
        output = {"id":self.id, "items_in_canvas":len(self.canvas.find_all())}
        return str(output)

class __Head_Navigator:  #Implementation de la gestion des positions

    """
    Point gestion

    Has forward, right, left, function calculus
    """

    def __init__(self, pos=(0,0), dire = 0):
        """
        create a head navigator

        keywords :
           - pos : initial pos (when reset will set to this point)
           - dir : same as pos but with dir
        """
        self.initX = self.x = pos[0]
        self.initY = self.y = pos[1]
        self.initDir = self.dir = math.radians(dire)

    def get(self):
        """
        return pos and dir in tuple as ((x,y), dir)
        """
        return ((self.x, self.y), self.dir)

    def forward(self, x):
        """
        Makes the point go forward by x pixels in dir
        """
        self.x = (self.x+(x*(math.cos(self.dir))))
        self.y = (self.y+(x*(math.sin(self.dir))))
        return (self.x, self.y)

    def left(self, angle):
        """
        Rotate dir by "angle" degrees left
        """
        self.dir -= math.radians(angle)
    def right(self, angle):
        """
        Same as left but by angle degrees right
        """
        self.dir += math.radians(angle)
    def rotate(self, angle):
        """
        Duplicate of right
        """
        self.right(angle)

    def reset(self):
        """
        reset the x, y and dir attributes

        set them to the given pos at creation (0 by default)
        """
        self.x = self.initX
        self.y = self.initY
        self.dir= self.initDir

#Classe gestion de buffering, peut etre améliorée


class __Item_Change_Buffer:

    """
    Buffer gestion

    TODO: upgraded item stocking
    No size limit by default (memory leak?)
    """
    def __init__(self, size=-1):
        self.buff = []; self.size = size
    def is_empty(self):
        """
        check if buffer is empty
        """
        return self.buff==[]
    def pop(self):
        """
        remove an item from buffer and return it
        """
        return self.buff.pop(-1)
    def add(self, item):
        """
        add an item to the buffer
        """
        if len(self.buff)==self.size: self.buff.pop(0)
        self.buff.append(item)





class Navigator(__Head_Navigator):

    """
    Navigator used to navigate in screen

    (extends Head Navigator)
    can be shown on screen
    """

    __obj_counter = 0

    def __init__(self, pos=(0,0), dire = 0, shown=False):

        _HN.__init__(self, pos, dire)

        Navigator.__obj_counter +=1
        self.id = "Navigator_"+str(Navigator.__obj_counter)

        self.w = getScreen()
        self.shown = shown

        self.show()

    def link(self, other, couleur="black", epaisseur=LINE_WIDTH):
        debug((*_HN.get(self)[0], *_HN.get(other)[0]))
        self.w.canvas.create_line(*_HN.get(self)[0], *_HN.get(other)[0],  width=epaisseur,
                                  smooth=0, fill = couleur)
        self.w.update()

    def forward(self, x):
        _HN.forward(self, x)
        if self.shown: self.show()

    def show(self):
        if self.shown :
            self.w.canvas.delete(self.id)
            Pen.cercle(self, 5)
        self.w.update()

class Pen(__Head_Navigator, __Item_Change_Buffer):

    """
    Pen to draw on canvas
    implements head navigator and item buffer
    """
    __name__ = "Pen"
    __obj_count__ = 0

    def __init__(self, pos = (0,0), direction = 0):


        _HN.__init__(self, pos, direction)
        _ICB.__init__(self)

        Pen.__obj_count__ += 1
        self.id = "Pen_"+str(Pen.__obj_count__)

        self.w = getScreen()
        self.color = "black"
        debug(("got it,", self.w))


    def __setDefault__(self, kwargs, output, kw, trslt, dflt):
        if kw in kwargs: output[trslt]=kwargs[kw]
        else : output[trslt]=dflt

    def __getOptions__(self, kwargs):
        output = {}
        return output

    def cercle(self, r, couleur="", contour="black", epaisseur=LINE_WIDTH):

        debug((r, couleur, contour, epaisseur, self.id), "DRAWING")

        self.w.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r,
                             fill=couleur, outline=contour, width=epaisseur, tag=self.id)
        self.w.update()

    def dirty_circle(self, r, pas, couleur="", contour="black", epaisseur=LINE_WIDTH):
        for x in range(pas):
            _HN.right(self, 360/pas)
            forward(r)
        debug((r, couleur, contour, epaisseur, self.id), "DRAWING")
        self.w.update()


    def logo(self, taille, pas):
        for x in range(pas):
            _HN.right(self, 360/pas)
            dirty_circle(taille, pas)
        self.w.update()

    def forward(self, x, epaisseur=LINE_WIDTH):

        self.buff.append(
            self.w.canvas.create_line(*_HN.get(self)[0], *_HN.forward(self, x),
                                      tag = self.id, width=epaisseur, smooth=True, fill = self.color)
            )
        self.w.update()

    def reset(self):
        """ reset pos"""
        _HN.reset(self)

    def undo(self):
        """
        undo pen drawing

        TODO: implement pos undo
        """
        self.w.canvas.delete(_ICB.pop(self))
        self.w.update()

    def setColor(self, color):
        """set pen color"""
        self.color = color
    def setLineWidth(self, width):
        """set pen width"""
        self.lineWidth = width


#Raccourci pour accès classe
_HN = __Head_Navigator
_ICB = __Item_Change_Buffer

# =============================================================== GLOBALS FUNCTIONS ====================================================


###Permet de faire forward(x) au lieu de p.forward(x)###


#Creation d'une fonction qui sera ensuite adapté grace a un format().
#Ce texte sera ensuite compilé dans la zone "global" afin d'etre accessible directement.
#L'interet de ces deux fonctions est de pouvoir ajouter des fonctionnalités sans modification
#Et sans code tres repetitif;

# ---------------------------------------------------------------- FUNCTION FORMAT ----------------------------------------------------------


#Ce string est le modèle utilisé lors du format. Il définit une fonction avec un nom et des arguments
# Test si l'objet est Null auquelle cas il l'initialise puis appelle la méthode voulue avec les arguments
# Donné lors de l'appel initial

func_format = """\
def {name}({args}):
    global {obj}
    if {obj}==None: {obj} = {cls}()
    try:
        return {obj}.{name}({args_name})
    except: raise PAP_Error("Error", sys.exc_info())
"""

# ---------------------------------------------------------------- ARGUMENTS GETTING ----------------------------------------------------------


# Cette fonction est un generateur qui prend une liste et yield chacune des valeurs de celle ci
# sauf si c'est string auquel cas il lui ajoute des ["].

def some_iter(l):
    for x in l:
        if isinstance(x, str):
            yield '"'+x+'"'
        else: yield x

#Fonction chiante a decrire

def get_args_list(func):

    a, var, kwarg, b = inspect.getargspec(func)  #Output -> args
    if b:
        b = [x for x in some_iter(b)]
        output = a[1:len(a)-len(b)]+list(map(lambda x:"%s=%s" %(x[0], x[1]),  #Cette ligne a pour but d'ajouter les premiers argument sans valeur par defaut, et d'assembler
                                 (zip(a[len(a)-len(b)::1], b))))              #Les arguments avec des valeurs par defaut. Le zip fait des tuple de a[n], b[n]. La lambda le depack et en fait un "{argname}={defaultvalue}"
    else: output = a[1::1]
    default = a[1::1]
    if var:
        temp ="*%s" %(var);output.append(temp);default.append(temp)
    if kwarg:
        temp="**%s" %(kwarg);output.append(temp);default.append(temp)
    return output, default


# ---------------------------------------------------------------- FUNCTION CREATIONS ----------------------------------------------------------

# Cette fonction recupere une liste de fonction et une classe.
# Puis génère pour chaque méthode de la liste une fonction en global
# Qui se refere a un objet créée pour l'occasion
# Son nom par défaut est "_"+clss.__name__ :
# EX : _Screen, _Pen, etc
# Mais peut etre modifié

def construct_func(funcs, clss, varName = None): #La classe entrée doit posséder un attribut __name__
    if varName == None: varName = "_"+clss.__name__
    debug(varName)
    exec("%s = None"%(varName), globals())
    for funcname in funcs:
        func = getattr(clss, funcname)
        args_entry, args = get_args_list(func)
        exec(func_format.format(name=funcname, args = ",".join(args_entry),
                                args_name = ",".join(args), cls=clss.__name__, obj=varName),
             globals())

def init():

    construct_func(__funcs_screen, Screen)
    construct_func(__funcs_pen, Pen)

def reset():
    _Screen.reset()
    _Pen.reset()

if __name__ == "__main__": init()
else:init()
