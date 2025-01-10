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







if __name__ == '__main__':
    app.run() 