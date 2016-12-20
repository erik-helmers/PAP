from tkinter import *
import tkinter.filedialog as tkFD
import tkinter.messagebox as tkMB

from main import *
import main

import colorizedInterface as clrI

import sys

hello = lambda : (self.root.quit(),print("geak,egkg, hrgbahgb "))

      
def notImplemented(*args, **kargs):
      tkMB.showerror(title = "Error", message="This function is not yet implemented")
      return



class PAPIDE:

   __counter__ = 0
   
   def __init__(self, filename = None):

      self.root = Tk()
      if filename == None: self.root.title("Rien du tout du tout")
      else: self.root.title(filename)

      
      PAPIDE.__counter__ += 1
      self.id = "PAPIDE window n°%s" %(PAPIDE.__counter__)

      # ==================================== CONFIGURATION DE L'EDITOR ET DE L'OUTPUT ================================================
      
      editor = clrI.PAPEditor(self.root)
      editor.grid(sticky = N+S+E+W)

      self.entry = editor.entry

      self.screen = Screen(self.root)
      self.screen.grid(row = 0, column = 1, sticky = E+W+N+S)
      
      self.root.grid_rowconfigure(0, weight=1)
      self.root.grid_columnconfigure(0, weight=1)
      self.root.grid_columnconfigure(1, weight=100)
      
      main._Screen = self.screen
      
      
      # =========================================== CONFIGURATION DE LA BARRE DE MENU ============================================
      # =============================================== ET DES RACCOURCIS CLAVIERS ===============================================
      
      menubar = Menu(self.root)
      
      # On créé un "pulldown menu" File et on l'ajoute au menubar
      filemenu = Menu(menubar, tearoff=0)

      filemenu.add_command(label="Open", command=self.openFile) #On lie le bouton Open avec la commande openFile
      filemenu.add_command(label="Save", command=self.saveFile) #Idem mais avec Save et saveFile
      filemenu.add_command(label="Save As", command=self.saveAsFile) # Toujours pareil on assigne le bouton Save As a saveAsFile
      filemenu.add_separator()
      filemenu.add_command(label="Exit", command=self.leave) #Exit quitte l'IDE
      self.root.protocol("WM_DELETE_WINDOW", self.leave)
      menubar.add_cascade(label="File", menu=filemenu)  # On affiche le menu File a la barre

      # create more pulldown menus
      editmenu = Menu(menubar, tearoff=0) # Idem avec edit
      editmenu.add_command(label="Cut", command=notImplemented)
      editmenu.add_command(label="Copy", command=notImplemented)
      editmenu.add_command(label="Paste", command=notImplemented)
      menubar.add_cascade(label="Edit", menu=editmenu)

      runmenu = Menu(menubar, tearoff=0) # Idem 

      runmenu.add_command(label="Run module -> F5", command=self.executeCode) #Ici on lie Run module avec l'éxuction complete du code
      self.entry.bind("<F5>", self.executeCode) # Le boutton F5 est le raccourci pour Run module

      menubar.add_cascade(label="Run", menu=runmenu)

      helpmenu = Menu(menubar, tearoff=0) #Toujours la meme chose
      helpmenu.add_command(label="About", command=hello)
      menubar.add_cascade(label="Help", menu=helpmenu)

      # display the menu
      self.root.config(menu=menubar) # Ici on informe a la fenetre principale que la barre de menu est menubar


      # ================================================ VARIABLES DIVERSES ==========================================================

      self.filename = None
      self.entry.focus_set()
      self.root.mainloop()
      
      # ================================================= GESTION DES FICHIERS =======================================================

   def setFileName(self, s):
      self.root.title(s)
      self.filename = s


      # ----------------------------------------------------- OPEN FILE --------------------------------------------------------------
      
   def openFile(self):

      """Cette fonction gere l'ouverture d'un fichier, et son chargement"""
      
      file = tkFD.askopenfile() # On créer une boite de dialog pour l'ouverture du fichier
      # Si aucun fichier n'est séléctionné, retourne None, sinon retourne un file

      if file == None: return # Si aucun fichier sélectionné, on ne peut pas le manipuler

      self.setFileName(file.name) # On sauvegarde le nom, afin de pouvoir sauvegarder
                             # Les modifications plus tard

      text = file.read() # On lit la totalité des characères du text
      self.entry.delete("1.0", END)
      self.entry.insert("1.0", text) # On ajoute le contenu du fichier a l'entry
      self.entry.colorize_all() # On le colorise

      file.close() # Une fois les opérations faite, on ferme le fichier


      # -------------------------------------------------- SAVE FILE -----------------------------------------------------------------
      
   def saveFile(self):
      
      if self.filename == None: self.saveAsFile() # Si on n'a pas de filename, saveAsFile
      
      else:
         
         entryText = self.entry.get("1.0", END) #Sinon on récupere le texte
         
         file = open(self.filename, mode = "w") #On ouvre le fichier, on écrase tout
         file.write(entryText) #On écrit tout le texte dedans
         file.close() # On le ferme


      # ----------------------------------------------- SAVE AS FILE ----------------------------------------------------------------
      
   def saveAsFile(self):

      file = tkFD.asksaveasfile() # On ouvre une boite de dialog pour la sauvegarde

      if file == None: return False# Si l'utilisateur n'a rien sélectionné on s'arrete

      self.setFileName(file.name) # On sauvegarde le nom de fichier
      
      file.write(self.entry.get("1.0", END)) # Sinon on écrit dedans

      file.close() # Puis on le ferme

      return True

      # ------------------------------------------------ LEAVE ----------------------------------------------------------------------
      
   def leave(self):

      text = self.entry.get("1.0", END)

      filename = self.filename
      
      if filename != None:
            file = open(filename)
            fileText= file.read()
            file.close()
      else: fileText = None
      if (filename == None and text == "\n") or (fileText == text):
            self.root.destroy()
            sys.exit()
            return

      else:
            save = tkMB.askyesnocancel("Sauvegarder ?", "Votre fichier n'a pas été sauvegardé. Sauvegarder ?")

            if save: self.saveFile(), self.root.destroy()
            elif save == None: return
            else: self.root.destroy()

# ======================================================= EXECUTION PART ==========================================================

      
   def executeCode(self, event=None):
      
      text =  self.entry.get("1.0", END)
      code = "".join([text]) #Au cas où, l'on devrait mettre

      exec(code, globals()) #On execute le code en contexte global.
      
if __name__ == "__main__":
   PAPIDE()
