from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Inicializacion del Servidor
app=Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='db_fruteria'
app.secret_key='mysecretkey'
mysql=MySQL(app)

#Declaracion de la ruta http://localhost:5000
@app.route('/')
def index():
    return render_template('frutaindex.html')

#Ruta http://localhost:5000/guardar tipo POST para insert
@app.route('/guardarFrutas', methods=['POST'])
def guardarFrutas():
    if request.method == 'POST':
        
        #pasamos a variables el contenido de los input 
        vnombre= request.form['txtNombre']
        vtemporada= request.form['txtTemporada']
        vprecio= request.form['txtPrecio']
        vstock= request.form['txtStock']
        #print(titulo,artista,anio) 
        
        #Conectar y ejecutar el insert
        cs = mysql.connection.cursor()
        cs.execute('insert into tb_frutas(fruta,temporada,precio,stock) values (%s,%s,%s,%s)', (vnombre,vtemporada,vprecio,vstock))
        mysql.connection.commit()
        
    flash('La fruta fue agregado correctamente')
    return redirect(url_for('index'))

@app.route('/eliminar_editar')
def eliminar_editar():
    consulta= mysql.connect.cursor()
    consulta.execute('select * from tb_frutas')
    conFrutas= consulta.fetchall()
    #print(conAlbums)
    return render_template('eliminar_editar_fruteria.html', frutas = conFrutas)

@app.route('/editarFruta/<id>')
def editar(id):
    cursorId=mysql.connection.cursor()
    cursorId.execute('select * from tb_frutas where id=%s',(id,))
    consId = cursorId.fetchone()
    return render_template('editarFruta.html', frutas=consId)

@app.route('/actualizarFruta/<id>',methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        vnombre= request.form['txtNombre']
        vtemporada= request.form['txtTemporada']
        vprecio= request.form['txtPrecio']
        vstock= request.form['txtStock']
        
        curAct = mysql.connection.cursor()
        curAct.execute('update tb_frutas set fruta= %s, temporada=%s, precio=%s, stock=%s where id=%s',(vnombre,vtemporada,vprecio, vstock,id))
        mysql.connection.commit()
    flash('Se actualizó la fruta'+vnombre)
    return redirect(url_for('eliminar_editar'))

@app.route('/eliminar/<id>')
def eliminar(id):
    cursorId=mysql.connection.cursor()
    cursorId.execute('select * from tb_frutas where id=%s',(id,))
    consId = cursorId.fetchone()
    return render_template('borrarFruta.html', frutas= consId)

@app.route('/delete/<id>',methods=['POST'])
def delete(id):
    if request.method == 'POST':
        varTitulo = request.form['txtTitulo']

        curAct = mysql.connection.cursor()
        curAct.execute('delete from tb_frutas where id=%s',(id))
        mysql.connection.commit()
    flash('Se borró el Album '+varTitulo)
    return redirect(url_for('eliminar_editar'))

@app.route('/Consult')
def Consult():
    return render_template('buscaFruta.html')

@app.route('/Consultanombre', methods=['POST'])
def consultanombre():
    Varbuscar= request.form['txtbuscar']
    print(Varbuscar)
    CC= mysql.connection.cursor()
    CC.execute('select * from tb_frutas where fruta LIKE %s', (f'%{Varbuscar}%',))
    confruta= CC.fetchall()
    print(confruta)
    return render_template('buscaFruta.html', listafruta = confruta)

if __name__ == '__main__':
    app.run(port=5000, debug=True)