from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='DB_Floreria'
app.secret_key='mysecretkey'
mysql=MySQL(app)


@app.route('/')
def index():
    consulta = mysql.connect.cursor()
    consulta.execute('select * from tbFlores')
    conExam= consulta.fetchall()
    return render_template('examen.html', examen = conExam)


@app.route('/guardar', methods=['POST'])
def guardar():
    if request.method == 'POST':
        

        vnombre= request.form['txtNombre']
        vcantidad= request.form['txtCantidad']
        vprecio = request.form['txtPrecio']

        cs = mysql.connection.cursor()
        cs.execute('insert into tbFlores(nombre,cantidad,precio) values (%s,%s,%s)', (vnombre,vcantidad,vprecio))
        mysql.connection.commit()
        
    flash('El registro fue agregado correctamente')
    return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    cursorId=mysql.connection.cursor()
    cursorId.execute('select * from tbFlores where id=%s',(id,))
    consId = cursorId.fetchone()
    return render_template('confirmar.html', flores= consId)

@app.route('/delete/<id>',methods=['POST'])
def delete(id):
    if request.method == 'POST':
        varNombre = request.form['txtNombre']

        curAct = mysql.connection.cursor()
        curAct.execute('delete from tbFlores where id=%s',(id))
        mysql.connection.commit()
    flash('Se borró el registro '+varNombre)
    return redirect(url_for('index'))

#Ejecucion de nuestro programa
if __name__ == '__main__':
    app.run(port=5000, debug=True)