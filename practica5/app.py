#Importacion del framework
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

#Inicializacion del Servidor
app=Flask(__name__)

#Configuracion de la conexion
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='dbflask'
app.secret_key='mysecretkey'
mysql=MySQL(app)

#Declaracion de la ruta http://localhost:5000
@app.route('/')
def index():
    consulta= mysql.connect.cursor()
    consulta.execute('select * from tbAlbums')
    conAlbums= consulta.fetchall()
    #print(conAlbums)
    return render_template('index.html', albums = conAlbums)

#Ruta http://localhost:5000/guardar tipo POST para insert
@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        
        #pasamos a variables el contenido de los input 
        vtitulo= request.form['txtTitulo']
        vartista= request.form['txtArtista']
        vanio= request.form['txtAnio']
        #print(titulo,artista,anio) 
        
        #Conectar y ejecutar el insert
        cs = mysql.connection.cursor()
        cs.execute('insert into tbAlbums(titulo,artista,anio) values (%s,%s,%s)', (vtitulo,vartista,vanio))
        mysql.connection.commit()
        
    flash('El album fue agregado correctamente')
    return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    cursorId=mysql.connection.cursor()
    cursorId.execute('select * from tbAlbums where id=%s',(id,))
    consId = cursorId.fetchone()
    return render_template('editaralbum.html', album=consId)

@app.route('/actualizar/<id>',methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        varTitulo = request.form['txtTitulo']
        varArtista = request.form['txtArtista']
        varAnyo = request.form['txtAnio']
        
        curAct = mysql.connection.cursor()
        curAct.execute('update tbAlbums set titulo= %s, artista=%s, anio=%s where id=%s',(varTitulo,varArtista,varAnyo,id))
        mysql.connection.commit()
    flash('Se actualozó el Album '+varTitulo)
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    cursorId=mysql.connection.cursor()
    cursorId.execute('select * from tbAlbums where id=%s',(id,))
    consId = cursorId.fetchone()
    return render_template('borraralbum.html', album= consId)

@app.route('/delete/<id>',methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        varTitulo = request.form['txtTitulo']
        
        curAct = mysql.connection.cursor()
        curAct.execute('delete from tbAlbums where id=%s',(id))
        mysql.connection.commit()
    flash('Se borró el Album '+varTitulo)
    return redirect(url_for('index'))

#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)