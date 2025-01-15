import sqlite3

# Conexión global
connection = sqlite3.connect("database/pychat.db", check_same_thread=False)
cursor = connection.cursor()



def userExist(email):
    sql = "SELECT 1 FROM users WHERE email = '%s' LIMIT 1;"%(email)
    cursor.execute(sql)
    result = cursor.fetchone()
    return result is not None


def register(email,password):
    try:
        sql = "INSERT INTO users (email,password) VALUES ('%s','%s')"%(email,password)
        cursor.execute(sql)
        # Guarda los cambios
        connection.commit()
        cursor.close()
        return True
    
    except sqlite3.Error as e:
        print("Operation Error:",e)


    


def login(email,password):
    try:
        cursor = connection.cursor()
        sql = "SELECT email, password FROM users WHERE email=? AND password=?"
        cursor.execute(sql, (email, password))
        result = cursor.fetchall()
        return result
    

    except sqlite3.Error as e:
        print("Operation Error:",e)

    connection.commit()
    cursor.close()
