from cons import *
import sys, time, inspect, math

if sys.version_info[0] == 2:  # Just checking your Python version to import Tkinter properly.
    from Tkinter import *
else:
    from tkinter import *


_funcs_screen_ = ["toggle_fullscreen", "end_fullscreen", "leave", "background"]

class PAP_Error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def debug(s, t="ALL"):
    try:
        if DEBUG[t]or DEBUG["ALL"]:
            print(s)
    except KeyError: print("Unknown type %s, passing debug" %(t))


    
class MWindow:

    def __init__(self):
            
        #Parametres de FullScreen
        self.fullscreen = FULLSCREEN
        
        self.tk = Tk() #Root
        self.frame = Frame(self.tk)
        self.frame.pack()
        
        #Binding 
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.bind("<Configure>", self.reconfig)
        
        self.tk.protocol("WM_DELETE_WINDOW", self.leave)
        
        if FULLSCREEN :self.toggle_fullscreen()
        
        self.canvas = Canvas(self.tk, width = 800, height = 800, bg="white")
        self.canvas.pack(expand=True, fill='both')
            
            
    def toggle_fullscreen(self, event=None):
        self.state = True  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "done"
    
    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", self.state)
        return "done"

    def switch_fullscreen(self):
        self.state = not self.state
        self.tk.attributes("-fullscreen", self.state)
        return self.state

    
    def leave(self, event=None):
        if not CONFIRM_QUIT or messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter ? #Tristesse"):
            self.tk.destroy()
        
    def __reconfig__(self, event):
        x, y = event.width//2, event.height//2
        self.canvas.config(scrollregion=(-x, -y, x, y))

    def background(color):
        if isinstance(color, (int, int, int)):
            pass
        
        
class _Head_Navigator:

    def __init__(self, pos=(0,0), dire = 0):

        self.x = pos[0]
        self.y = pos[1]
        self.dir = math.radians(dire)

    def forward(self, x):

        self.x = (self.x+(x*(math.cos(self.dir))))
        self.y = (self.y+(x*(math.sin(self.dir))))
        return (self.x, self.y)

    def left(angle): self.dir -= math.radians(dire)
    def right(angle): self.dir += math.radians(dire)
    def rotate(angle): right(angle)


class Pen(_Head_Navigator):

    def __init__(self, pos = (0,0), direction = 0):

        self.pos = pos
        self.direction = direction

        self.w = _Screen
        debug(("got it,", self.w))
        
    
    def cercle(self, r, couleur = "", contour = "black", epaisseur=LINE_WIDTH):
        
        debug((r, couleur, contour, epaisseur), "PEN")
        self.w.canvas.create_oval(self.x-r, self.y-r, self.x+r, self.y+r,
                             fill=couleur, outline=contour, width=epaisseur)



###Permet de faire forward(x) au lieu de p.forward(x)###


_Screen = None
_DfltPen = None


#Creation d'une fonction qui sera ensuite adapté grace a un format().
#Ce texte sera ensuite compilé dans la zone "global" afin d'etre accessible directement.
#L'interet de ces deux fonctions est de pouvoir ajouter des fonctionnalités sans modification
#Et sans code tres repetitif;

func_format = """\
def {name}({args}):
    global a
    if {obj}==None: {obj} = {cls}()
    try:
        return {obj}.{name}({args_name})
    except e: raise PAP_Error("Error", e)   
"""

def get_args_list(func):

    a, var, kwarg, b = inspect.getargspec(func)  #Output -> args
    if b:
        output = a[1:len(a)-len(b)]+list(map(lambda x:"%s=%s" %(x[0], x[1]),  #Cette ligne a pour but d'ajouter les premiers argument sans valeur par defaut, et d'assembler 
                                 (zip(a[len(a)-len(b)::1], b))))              #Les arguments avec des valeurs par defaut. Le zip fait des tuple de a[n], b[n]. La lambda le depack et en fait un "{argname}={defaultvalue}" 
    else: output = a[1::1]
    default = a[1::1]
    if var:
        temp ="*%s" %(var);output.append(temp);default.append(temp)
    if kwarg:
        temp="**%s" %(kwarg);output.append(temp);default.append(temp)
    return output, default

def construct_func(funcs, obj_name):
    exec("obj = %s"%(obj_name), globals())
    clss = obj.__class__
    for funcname in funcs:
        func = getattr(clss, funcname)
        args_entry, args = get_args_list(func)
        exec(func_format.format(name=funcname, args = ",".join(args_entry),
                                args_name = ",".join(args), cls=clss.__name__, obj=obj_name),
             globals())


    
