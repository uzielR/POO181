from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user,login_required, logout_user, current_user,UserMixin

app=Flask(__name__)
app.secret_key= 'mysecretkey'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='dbConsultorio'
app.secret_key='mysecretkey'
mysql=MySQL(app) 

class User(UserMixin):
    def __init__(self, id, rfc, password):
        self.id = id
        self.rfc = rfc
        self.password = password

    def get_id(self):
        return str(self.id)
    
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(id):
    print("este es mi id: " + id)
    # cursor = connection.cursor() este sql server
    # print INSERT INTO `login` (`id`, `rfc`, `password`) VALUES ('1', 'QWWQ123456', '123');
    #login del back
    cursor = mysql.connection.cursor() 
    cursor.execute('SELECT id, RFC, contraseña FROM Medicos WHERE id = %s', (id,))
    persona = cursor.fetchone()
    if persona:
        print("Metodo: load_user(id), el usuario si coincide.")
        #return User(id='1', email='121038198@upq.edu.mx', password='123')
        return User(id=persona[0], rfc=persona[1], password=persona[2])
    return None

@app.route('/')
def log():
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('log'))

@app.route('/login', methods=['POST'])
def login():
  
    if request.method == 'POST':
        rfc = request.form['rfc']
        password = request.form['contra']

        print("Metodo: login(), rfc y pass que llegan desde front: RFC {} pass {}".format(rfc, password))

        # cursor = connection.cursor()

        cursor = mysql.connection.cursor()
        query = 'SELECT id, RFC, contraseña FROM Medicos WHERE RFC = %s and contraseña = %s'
        cursor.execute(query, (rfc, password))  # Agrega comas después de cada valor
        persona = cursor.fetchone()
        print(persona)

        print("Metodo: rfc(), antes de validar rfc y pass")
        if persona:
            print("Metodo: login(), rfc y pass correctos")
            user = User(id=persona[0], rfc=persona[1], password=persona[2])
            flash('CONECTADO')
            print('CONECTADO')
            login_user(user)
            return redirect(url_for('inicio'))
        else:
            print("Usuario o Contraseña Incorrectas")
            flash('Usuario o Contraseña Incorrectas')
            return render_template('login.html')
    else:
        print("Datos login incompletos")
        return render_template('login.html')



@app.route('/inicio')
@login_required
def inicio():
    consulta= mysql.connect.cursor()
    consulta.execute('select Pacientes.id,concat(Medicos.nombre," ",Medicos.ap," ",Medicos.am),concat(Pacientes.nombre," ",Pacientes.ap," ",Pacientes.apellidoM),fechaNac,Pacientes.enfermedades,Pacientes.alergias,Pacientes.antecedentes from Pacientes inner join Medicos on Medicos.id=Pacientes.medicoA')
    conAlbums= consulta.fetchall()
    #print(conAlbums)
    
    return render_template('inicio.html',lsConsulta = conAlbums)

@app.route('/registroPaciente')
@login_required
def registroPaciente():
    consulta= mysql.connect.cursor()
    consulta.execute('select id,concat(Medicos.nombre," ",Medicos.ap," ",Medicos.am) from Medicos')
    conAlbums= consulta.fetchall()
    return render_template('registroPaciente.html', lsRegistro=conAlbums)

@app.route('/guardarPacientes', methods=['GET','POST'])
def guardarPacientes():
    if request.method == 'POST':
        cs= mysql.connection.cursor()
        VMedico = request.form['Medico']
        VNombre=request.form['txtNombre']
        VApellido_paterno=request.form['txtAP']
        VApellido_materno=request.form['txtAM']
        VFecha_de_nacimiento=request.form['txtNacimiento']
        VEnfermedades=request.form['txtEnfermedades']
        VAlergias=request.form['txtAlergias']
        VAntecedentes=request.form['txtAntecedentes']
        
        
        cs.execute('insert into Pacientes(medicoA,nombre,ap,apellidoM,fechaNac,enfermedades,alergias,antecedentes) values(%s,%s,%s,%s,%s,%s,%s,%s)',
        (VMedico,VNombre,VApellido_paterno,VApellido_materno,VFecha_de_nacimiento,VEnfermedades,VAlergias,VAntecedentes))
        mysql.connection.commit()
        
        
    flash('El doctor fue agregado correctamente')
    return redirect(url_for('inicio'))

@app.route('/exploracion')
@login_required
def exploracion():
    consulta= mysql.connect.cursor()
    consulta.execute('select id,concat(Pacientes.nombre," ",Pacientes.ap," ",Pacientes.apellidoM) from Pacientes')
    conAlbums= consulta.fetchall()
    return render_template('exploracion.html', lsRegistro=conAlbums)

@app.route('/guardarExploracion', methods=['GET','POST'])
def guardarExploracion():
    if request.method == 'POST':
        cs= mysql.connection.cursor()
        vPaciente = request.form['paciente']
        vFecha=request.form['txtFecha']
        vPeso=request.form['txtPeso']
        vAltura=request.form['txtAltura']
        vTemp=request.form['txtTemp']
        vLatidos=request.form['txtLatidos']
        vSaturacion=request.form['txtSaturacion']
        
        cs.execute('insert into Exploraciones(paciente,fecha,peso,altura,temperatura,latidos,saturacion) values(%s,%s,%s,%s,%s,%s,%s)',
        (vPaciente,vFecha,vPeso,vAltura,vTemp,vLatidos,vSaturacion))
        mysql.connection.commit()
    
    flash('La exploración fue agregada correctamente')
    return redirect(url_for('inicio'))

@app.route('/diagnostico')
@login_required
def citasConsultas():
    return render_template('diagnostico.html')

@app.route('/editar/<id>')
@login_required
def editar(id):
    cursorId=mysql.connection.cursor()
    cursorId.execute('select Pacientes.id,concat(Medicos.nombre," ",Medicos.ap," ",Medicos.am),Pacientes.nombre,Pacientes.ap,Pacientes.apellidoM,Pacientes.fechaNac,Pacientes.enfermedades,Pacientes.alergias,Pacientes.antecedentes from Medicos inner join Pacientes on Pacientes.MedicoA=Medicos.id  where Pacientes.id=%s',(id,))
    consId = cursorId.fetchone()
    return render_template('editarPaciente.html', rut=consId)

@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        cs= mysql.connection.cursor()
        vPaciente = request.form['txtNombre']
        vFecha=request.form['txtAP']
        vPeso=request.form['txtAM']
        vTemp=request.form['txtNacimiento']
        vLatidos=request.form['txtEnfermedades']
        vSaturacion=request.form['txtAlergias']
        vAntecedentes=request.form['txtAntecedentes']
        
        cs.execute('update Pacientes set nombre=%s,ap=%s,apellidoM=%s,fechaNac=%s,enfermedades=%s,alergias=%s,antecedentes=%s where id=%s',
        (vPaciente,vFecha,vPeso,vTemp,vLatidos,vSaturacion, vAntecedentes, id))
        print(vPaciente,vFecha,vPeso,vTemp,vLatidos,vSaturacion, vAntecedentes, id)
        mysql.connection.commit()
    
    flash('El paciente fue actualizado correctamente')
    return redirect(url_for('inicio'))

@app.route('/delete/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    conn = mysql.connection.cursor()
    conn.execute("DELETE FROM Pacientes WHERE id = %s", (record_id,))
    conn.commit()
    conn.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/expedientePacientes/<id>')
@login_required
def citasConsultas5(id):
    consulta= mysql.connect.cursor()
    consulta.execute('select Exploraciones.id,concat(Pacientes.nombre," ",Pacientes.ap," ",Pacientes.apellidoM),Exploraciones.fecha,Exploraciones.peso,Exploraciones.altura,Exploraciones.temperatura,Exploraciones.latidos,Exploraciones.saturacion from Pacientes inner join Exploraciones on Exploraciones.paciente= Pacientes.id where Pacientes.id='+id)
    conAlbums= consulta.fetchall()
    return render_template('expedientes.html',lsConsulta=conAlbums)

@app.route('/administracionMedicos2', methods=['GET','POST'])
def administracionMedicos2():
    if request.method == 'POST':
        
        #pasamos a variables el contenido de los input 
        vtitulo= request.form['nombre']
        vartista= request.form['apellido']
        vanio= request.form['correo']
        
        cs = mysql.connection.cursor()
        cs.execute('insert into Medicos(nombre,ap,correo) values (%s,%s,%s)', (vtitulo,vartista,vanio))
        mysql.connection.commit()
        
    flash('El doctor fue agregado correctamente')
    return render_template('Administracion medicos 2.html')








@app.route('/consultarPacientes')
def consultarPacientes():
    return render_template('Consultar Pacientes.html')

@app.route('/consultarPacientes2')
def consultarPacientes2():
    return render_template('Consultar Pacientes 2.html')

@app.route('/consultarPacientes3')
def consultarPacientes3():
    return render_template('Consultar Pacientes 3.html')

@app.route('/consultarPacientes4')
def consultarPacientes4():
    return render_template('Consultar Pacientes 4.html')


@app.route('/expedientePacientes2')
def expedientePacientes2():
    return render_template('Expediente Pacientes 2.html')

@app.route('/exploracion_diagnostico')
def exploracion_diagnostico():
    return render_template('Exploracion y diagnostico.html')

@app.route('/exploracion_diagnostico2')
def exploracion_diagnostico2():
    return render_template('Exploracion y diagnostico 2.html')

@app.route('/exploracion_diagnostico3')
def exploracion_diagnostico3():
    return render_template('Exploracion y diagnostico 3.html')

@app.route('/exploracion_diagnostico4')
def exploracion_diagnostico4():
    return render_template('Exploracion y diagnostico 4.html')

@app.route('/exploracion_diagnostico5')
def exploracion_diagnostico5():
    return render_template('Exploracion y diagnostico 5.html')


if __name__ == '__main__':
    app.run(port=5000, debug=True)