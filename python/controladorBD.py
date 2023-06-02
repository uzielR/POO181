from tkinter import messagebox
import sqlite3
import bcrypt


class controladorBD:
    def __init__(self):
        pass
    
    def conexionBD(self):
        try:
            conexion = sqlite3.connect(r'C:\Users\Edgar\OneDrive\Documentos\GitHub\POO181\python\bebidas.db')
            return conexion
        except sqlite3.OperationalError:
            print('No se puede conectar')
    
    def altaBD(self, nombre, clasificacion, marca, precio):
        conx=self.conexionBD()
        
        if (nombre == '' or clasificacion == '' or marca == '' or precio == ''):
            messagebox.showwarning('Aguas!!', 'Formulario incompleto')
            conx.close()
        else:
            #3. Realizar el insert a la BD
            #4. Preparamos las variables necesarias
            cursor= conx.cursor()
            
            datos=(nombre,clasificacion,marca,precio)
            sqlInsert=' insert into bebidasTB(nombre,clasificacion,marca,precio) values(?,?,?,?)'
            
            #5. Ejecutamos el insert
            cursor.execute(sqlInsert, datos)
            conx.commit()
            conx.close()
            messagebox.showinfo("Exito", 'Usuario guardado')
            
    def buscarBebida(self, id):
        
        #1. Realizar conexion BD
        conx = self.conexionBD()
        
        #2. Verificar que el id no esté vacio
        if(id==''):
            messagebox.showwarning('Cuidado','Escribe un identificador')
            conx.close()
        else:
            #3. Ejecutar la consulta
            try:
                #4. Preparamos lo necesario
                cursor= conx.cursor()
                sqlSelect = 'select * from bebidasTB where id= '+id
                
                #5. Ejectutamos, guardamos la consulta y cerramos conexion
                cursor.execute(sqlSelect)
                RSusuario= cursor.fetchall()
                conx.close()
                return RSusuario
                
            except sqlite3.OperationalError:
                print('Error de consulta')