from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from controladorBD import *

controlador = controladorBD()
#Metodo que usa mi objeto controlador para insertar
def ejectutaInsert():
    controlador.altaBD(varNom.get(), clasificacion.get(), marca.get(), varPrecio.get())
    varNom.set('')
    clasificacion.set('')
    marca.set('')
    varPrecio.set('')
#Funcion que usa mi objeto controlador para buscar 1 usuario

def ejecutarSelectU():
    rsUsu = controlador.buscarBebida(varBus.get())
    textBus.delete('1.0', END)

    #Iteramos el contenido de la consulta y lo guardamos en CADENA 
    for usu in rsUsu:
        cadena = str(usu[0])+' '+usu[1]+ ' '+usu[2] + ' '+ usu[3]+ ' '+str(usu[4])
    if (rsUsu):
        textBus.insert(INSERT, cadena)
    else:
        messagebox.showinfo('No encontrado', 'Usuario no existe en BD')

def ejecutarSelectU2():
    rsUsuario = controlador.buscarBebida(varElim.get())
    tree2.delete(*tree2.get_children())

    #Iteramos el contenido de la consulta y lo guardamos en CADENA 
    for usu in rsUsuario:
        cadena = tree2.insert('',tk.END, values=usu)
    if (rsUsuario):
        textBus.insert(INSERT, cadena)
    else:
        messagebox.showinfo('No encontrado', 'Usuario no existe en BD')

def ejecutarSelectU3():
    rsUsuario = controlador.buscarBebida(varAct.get())
    varNom1.set('')
    clasificacion2.set('')
    marca2.set('')
    varPrecio1.set('')
    
    if (rsUsuario):
        for usu in rsUsuario:
            varNom1.set(usu[1])
            clasificacion2.set(usu[2])
            marca2.set(usu[3])
            varPrecio1.set(usu[4])
    else:
        messagebox.showinfo('No encontrado', 'Usuario no existe en BD')

def ejecutarConsul():
    rsConsul = controlador.consultarBebida()
    tree.delete(*tree.get_children())
    for fila in rsConsul:
        tree.insert('',tk.END, values=fila)

def ejecutarModi():
    ask = messagebox.askyesno('Confirmación','¿Seguro que quiere actualizar esta información?')
    if ask == True:
        controlador.actualizarBebida(varAct.get(), varNom1.get(), clasificacion2.get(), marca2.get(), varPrecio1.get())
        varNom1.set('')
        clasificacion2.set('')
        marca2.set('')
        varPrecio1.set('')
    else:
        messagebox.showerror('Error', 'Usuario no Actualizado')
        

def ejecutarEliminarU():
    ask = messagebox.askyesno('Pregunta', '¿Seguro que quiere eliminar el usuario?')
    if ask == True:
        controlador.eliminarBebida(varElim.get())
        tree2.delete(*tree2.get_children())
        messagebox.showinfo('Info', 'Usuario Eliminado')
    else:
        messagebox.showerror('Error', 'Usuario no Eliminado')
        
def promedioBebidas():
    rsProm = controlador.promedio()
    varProm.set(rsProm)

def promedioBebidasMarca():
    rsProm1 = controlador.promedioMarca(marca1.get())
    varProm1.set(rsProm1)
    
def promedioBebidasClasi():
    rsProm2 = controlador.promedioClasi(clasificacion1.get())
    varProm2.set(rsProm2)
    

ventana = Tk()
ventana.title('CRUD de bebidas')
ventana.geometry('500x300')

panel= ttk.Notebook(ventana)
panel.pack(fill='both', expand='yes')

pestana1= ttk.Frame(panel)
pestana2= ttk.Frame(panel)
pestana3= ttk.Frame(panel)
pestana4= ttk.Frame(panel)
pestana5= ttk.Frame(panel)

# Pestaña1: Formulario de registro
titulo = Label(pestana1, text='Registro Bebidas', fg='blue', font=('Modern', 18)).pack()

varNom= tk.StringVar()
lblNom= Label(pestana1, text='Nombre: ').pack()
txtNom= Entry(pestana1, textvariable=varNom).pack()

lblClasificacion= Label(pestana1, text='Clasificacion: ').pack()
clasificacion = ttk.Combobox(
    pestana1,
    state="readonly",
    values=["Energizantes", "Agua", "Azucaradas", "Relajantes"]
)
clasificacion.pack()

lblmarca= Label(pestana1, text='Marca: ').pack()
marca = ttk.Combobox(
    pestana1,
    state="readonly",
    values=["Pepsi", "Coca-Cola", "Nescafe", "Lipton"]
)
marca.pack()

varPrecio= tk.StringVar()
lblPrecio= Label(pestana1, text='Precio: ').pack()
txtPrecio= Entry(pestana1, textvariable=varPrecio).pack()

btnGuardar= Button(pestana1, text='Guardar Bebida', command=ejectutaInsert).pack()

#Pestaña 2: Buscar Usuario

titulo2= Label(pestana2, text='Buscar Bebida', fg='green', font=('Modern', 18)).pack()

varBus= tk.StringVar()
lblid=Label(pestana2,text='Identificador de bebida:').pack()
txtid= Entry(pestana2,textvariable=varBus).pack()
btnBusqueda= Button(pestana2,text='Buscar', command=ejecutarSelectU).pack()

subBus= Label(pestana2, text='Resgistrado:', fg='blue',font=('Modern', 15)).pack()
textBus= tk.Text(pestana2, width=52, height=5)
textBus.pack()

#Pestaña 3: Consultar Usuario
titulo3 = Label(pestana3, text='Consultar Bebidas', fg = 'purple', font=('Modern', 18)).pack()
tree = ttk.Treeview(pestana3, column=("c1", "c2", "c3", 'c4', 'c5'), show='headings')

tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text="ID")

tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text="Nombre")

tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text="Clasificacion")

tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text="Marca")

tree.column("#5", anchor=tk.CENTER)
tree.heading("#5", text="Precio")

tree.pack()
btnConsul= Button(pestana3,text='Consultar', command=ejecutarConsul).pack()

varProm=tk.StringVar()
lblProm= Label(pestana3, text='Promedio de bebidas: ').pack()
txtProm= Entry(pestana3, textvariable=varProm).pack()
btnProm= Button(pestana3,text='Consultar', command=promedioBebidas).pack()

lblProm1= Label(pestana3, text='Promedio de bebidas por marca: ').pack()
lblmarca1= Label(pestana3, text='Marca: ').pack()
marca1 = ttk.Combobox(
    pestana3,
    state="readonly",
    values=["Pepsi", "Coca-Cola", "Nescafe", "Lipton"]
)
marca1.pack()


varProm1=tk.StringVar()

txtProm1= Entry(pestana3, textvariable=varProm1).pack()
btnProm1= Button(pestana3,text='Consultar', command=promedioBebidasMarca).pack()

lblProm2= Label(pestana3, text='Promedio de bebidas por clasificacion: ').pack()
lblClasificacion1= Label(pestana3, text='Clasificacion: ').pack()
clasificacion1 = ttk.Combobox(
    pestana3,
    state="readonly",
    values=["Energizantes", "Agua", "Azucaradas", "Relajantes"]
)
clasificacion1.pack()

varProm2=tk.StringVar()

txtProm2= Entry(pestana3, textvariable=varProm2).pack()
btnProm2= Button(pestana3,text='Consultar', command=promedioBebidasClasi).pack()

#Pestaña 4
titulo4 = Label(pestana4, text='Eliminar Bebidas', fg = 'black', font=('Modern', 18)).pack()

varElim= tk.StringVar()
lblP4=Label(pestana4,text='Identificador de Usuario:').pack()
txtP4= Entry(pestana4,textvariable=varElim).pack()
btnBusqueda= Button(pestana4,text='Buscar', command=ejecutarSelectU2).pack()
btnElim= Button(pestana4,text='Eliminar', command=ejecutarEliminarU).pack()

tree2 = ttk.Treeview(pestana4, column=("c1", "c2", "c3", 'c4','c5'), show='headings')

tree2.column("#1", anchor=tk.CENTER)
tree2.heading("#1", text="ID")

tree2.column("#2", anchor=tk.CENTER)
tree2.heading("#2", text="Nombre")

tree2.column("#3", anchor=tk.CENTER)
tree2.heading("#3", text="Clasificacion")

tree2.column("#4", anchor=tk.CENTER)
tree2.heading("#4", text="Marca")

tree2.column("#5", anchor=tk.CENTER)
tree2.heading("#5", text="Precio")

tree2.pack()

#Pestaña 5
titulo5 = Label(pestana5, text='Actualizar Bebidas', fg = 'black', font=('Modern', 18)).pack()

varAct= tk.StringVar()
lblP4=Label(pestana5,text='Identificador de Bebida:').pack()
txtP4= Entry(pestana5,textvariable=varAct).pack()
btnBusqueda= Button(pestana5,text='Buscar', command=ejecutarSelectU3).pack()



varNom1= tk.StringVar()
lblNom1= Label(pestana5, text='Nombre: ').pack()
txtNom1= Entry(pestana5, textvariable=varNom1).pack()

lblClasificacion2= Label(pestana5, text='Clasificacion: ').pack()
clasificacion2 = ttk.Combobox(
    pestana5,
    state="readonly",
    values=["Energizantes", "Agua", "Azucaradas", "Relajantes"]
)
clasificacion2.pack()

lblmarca2= Label(pestana5, text='Marca: ').pack()
marca2 = ttk.Combobox(
    pestana5,
    state="readonly",
    values=["Pepsi", "Coca-Cola", "Nescafe", "Lipton"]
)
marca2.pack()

varPrecio1= tk.StringVar()
lblPrecio1= Label(pestana5, text='Precio: ').pack()
txtPrecio1= Entry(pestana5, textvariable=varPrecio1).pack()

btnAct= Button(pestana5,text='Actualizar', command=ejecutarModi).pack()


panel.add(pestana1, text='Agregar bebida')
panel.add(pestana2, text='Buscar bebida')
panel.add(pestana3, text='Consultar bebida')
panel.add(pestana4, text='Eliminar bebida')
panel.add(pestana5, text='Actualizar bebida')


ventana.mainloop()