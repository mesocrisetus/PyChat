from flask import Flask, render_template,url_for,request,redirect,flash
import db_modules as dbModules
import os

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
        return render_template('index.html')

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
    









if __name__ == '__main__':
    app.run() 