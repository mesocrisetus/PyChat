from flask import Flask, render_template,url_for,request,redirect,flash
import db_modules as dbModules
import os
from datetime import datetime

#App Config
app = Flask(__name__)

#SecretKey

app.secret_key =os.urandom(24)

@app.route("/")
def loginForm():
    
    return render_template("login.html")

@app.route("/loginIn",methods=['POST'])
def loginIn():
    email = request.form['email']
    password = request.form['password']
    loginCheck = dbModules.login(email,password)

    if loginCheck:
        userId = loginCheck[0]
        users = dbModules.getAllUsers()
        users = [user for user in users if user[1] != email]
        return render_template('index.html',email=email,userId=userId,users=users)

    else:
        pass

    message = "Usuario o contraseña incorrecta."
    flash(message)
    return render_template("login.html")

#Register

@app.route("/registerForm")
def registerForm():
    return render_template("registerForm.html")


@app.route("/register",methods=['POST'])
def register():

    email = request.form['email']
    password = request.form['password']
    password2 = request.form['password2']

    if password != password2:
        message = "Las contraseñas no coinciden."
        flash(message)
        return render_template('registerForm.html')
    
    userExist = dbModules.userExist(email)

    if userExist:
        message = "El usuario ya se encuentra registrado"
        flash(message)
        return render_template('registerForm.html')
    
    else:
        registerUser = dbModules.register(email,password)
        if registerUser:
            message = "El usuario se ha registrado correctamente"
            flash(message)
            return render_template('login.html')
        

@app.route('/chat/<int:userId>')
def chat(userId):    
    user2Id = request.args.get('user2')
    room = dbModules.get_room(userId, user2Id) 
    if not room:
        # Si la sala no existe, crearla
        room_id = dbModules.create_room(userId, user2Id)
    else:
        room_id = room[0]
    messages = dbModules.get_messages(room_id)
    print(messages)
    users = dbModules.getAllUsers()

    return render_template('index.html', roomId=room_id, messages=messages, userId=user2Id,users=users)

@app.route('/sendMessage', methods=['POST'])
def send_message():
    url = request.form.get('current_url')
    room_id = request.form['roomId']
    user_id = request.form['userId']
    message_text = request.form['chatInput']
    
    # Obtener la fecha y hora actual    
    message_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insertar el mensaje en la base de datos
    dbModules.send_message(user_id, room_id, message_text, message_date)

    # Redirigir de nuevo a la página de chat con los mensajes actualizados
    return redirect(url)

@app.route('/logout')
def logout():

    return redirect('/')  # Redirige a la página de inicio de sesión




if __name__ == '__main__':
    app.run() 