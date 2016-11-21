import _tkinter
from Tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, Checkbutton
import Tkinter

from Lib.DAO.Strategy.Query import Query
from Lib.DAO.Strategy.Statements import And,Or,Like

from App.Models.Entrada import back_end_entrada
from App.Models.Evento import back_end_evento
from App.Models.Asiento import back_end_asiento
from App.Models.Sector import back_end_sector

def vaciarPantalla(self):
    # vacio toda la pantalla
    for label in self.grid_slaves():
        label.grid_forget()
        
def inicioPantalla(self):   
    # agrego el titulo Datos  
    i = 0 
    Tkinter.Label(root, text="Datos", font = "Helvetica 16 bold italic").grid(row=i,sticky = W)
    i += 1
           
def agregarDatos(self,filtroTelefono,filtroDocumento,i):
    #print " en agregarDatos, filtroTelefono: {} filtroDocumento: {}".format(filtroTelefono,filtroDocumento)    
    Tkinter.Label(root, text="Telefono").grid(row=i, sticky=W)
    #vcmd = root.register(root.validate) # we have to wrap the command
    #e1 = Entry(root, validate="key", validatecommand=(vcmd, '%P'))    
    telefono = Entry(root)   
    telefono.grid(row=i, column=1)
    telefono.insert(END, filtroTelefono)
    i += 1
    
    Tkinter.Label(root, text="Documento").grid(row=i, sticky=W)
    documento = Entry(root)
    documento.grid(row=i, column=1) 
    documento.insert(END, filtroDocumento)
    Tkinter.Label(root, text=" ").grid(row=i, column=2, sticky=W)
    root.add_button = Button(root, text="Buscar", command=lambda: buscar(root,telefono,documento)).grid(row=i, column=3)
    i += 1


def buscar(self,telefono,documento):    
    E = back_end_entrada()
    self.filtroTelefono = telefono.get()
    self.filtroDocumento = documento.get()
    #print " en buscar, filtroTelefono: {} filtroDocumento: {}".format(self.filtroTelefono,self.filtroDocumento)
    
    vaciarPantalla(self)

    inicioPantalla(self)
    i = 1

    if not self.filtroTelefono:
        Tkinter.Label(root, text="Debe ingresar Telefono",fg="red",font = "bold").grid(row=i, sticky=W, columnspan=10)
        i += 1
    if not self.filtroDocumento:
        Tkinter.Label(root, text="Debe ingresar Documento",fg="red",font = "bold").grid(row=i, sticky=W, columnspan=10)
        i += 1

    if self.filtroTelefono and self.filtroDocumento:
        Q = Query(E)
        Q.add(And("telefono",self.filtroTelefono))
        Q.add(And("documento",self.filtroDocumento))
                
        entrada = E.fetchAll(Q)
        if entrada: 
            agregarDatos(self,self.filtroTelefono,self.filtroDocumento,i)
            i += 2
            armarPantalla(self,entrada,i) 
        else:
            Tkinter.Label(root, text="Los datos ingresados no se corresponden con una entrada valida",fg="red",font = "bold").grid(row=i, sticky=W, columnspan=10)
            i += 1
            agregarDatos(self,self.filtroTelefono,self.filtroDocumento,i)
    else:
        agregarDatos(self,self.filtroTelefono,self.filtroDocumento,i)           

def armarPantalla(root,entrada,i):
    Tkinter.Label(root, text="").grid(row=i)
    i += 1
    Tkinter.Label(root, text="Entrada", font = "Helvetica 16 bold italic").grid(row=i)
    i += 1
    for e in entrada: #deberia ser una sola...
        Tkinter.Label(root, text= "Telefono", borderwidth=5 ).grid(row=i,column=0) 
        Tkinter.Label(root, text= e.get("telefono"), borderwidth=5 ).grid(row=i,column=1) 
        i += 1
        Tkinter.Label(root, text= "Documento", borderwidth=5 ).grid(row=i,column=0) 
        Tkinter.Label(root, text= e.get("documento"), borderwidth=5 ).grid(row=i,column=1) 
        i += 1
        Tkinter.Label(root, text= "Evento", borderwidth=5 ).grid(row=i,column=0) 
        Evento = getEntidad(back_end_evento(), e.get("Evento_id"))
        Tkinter.Label(root, text= Evento.nombre, borderwidth=5 ).grid(row=i,column=1) 
        i += 1
        Asiento = getEntidad(back_end_asiento(), e.get("Asiento_id"))
        Sector = getEntidad(back_end_sector(), Asiento.Sector_id)
        Tkinter.Label(root, text= "Asiento", borderwidth=5 ).grid(row=i,column=0) 
        Tkinter.Label(root, text= "{} - {}".format(Sector.nombre,Asiento.numero), borderwidth=5 ).grid(row=i,column=1) 
        i += 1
        Tkinter.Label(root, text= "usada", borderwidth=5 ).grid(row=i,column=0) 
        usadaVar = Tkinter.IntVar()
        usada = Checkbutton(root, variable=usadaVar)
        usada.grid(row=i,column=1)
        used = e.get("usada")
        if used:
            usada.select()
        else:
            usada.deselect()
        i += 1
        root.add_button = Button(root, text="Actualizar", command=lambda: actualizar(root,e,usadaVar)).grid(row=i, column=3)
        i += 1

def getEntidad(E, id):
    Q = Query(E)
    Q.add(And(field = "id", value = id))
    if E.loadQuery(Q):
        return E
    return None
     
def actualizar(self,e,usadaVar):
    E = back_end_entrada()
    Q = Query(E)
    Q.add(And(field = "id", value = e.get("id")))
    E.loadQuery(Q)
    Q2 = Query(E)
    Q2.add(And(field = "id",value = e.get("id")))
    E.usada = usadaVar.get()
    E.save() 
    #devuelvo cartel de exito y vacio pantalla dejando solo para ingresar telefono y documento.    
    self.filtroDocumento = ""
    self.filtroTelefono = ""
    
    vaciarPantalla(self)
    inicioPantalla(self)
    i = 1
    Tkinter.Label(self, text="La entrada se actualizo con exito",fg="darkgreen",font = "bold").grid(row=i, sticky=W, columnspan=10)
    i += 1
    agregarDatos(self,self.filtroTelefono,self.filtroDocumento,i)    
        
#comienza la pantalla de la boleteria

root = Tkinter.Tk()

root.filtroDocumento = ""
root.filtroTelefono = ""

inicioPantalla(root)
i = 1
agregarDatos(root,root.filtroTelefono,root.filtroDocumento,i)

root.geometry("500x400")
root.mainloop()