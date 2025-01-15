import sqlite3

# Global connection
connection = sqlite3.connect("database/pychat.db", check_same_thread=False)
cursor = connection.cursor()


#Login and register

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
        sql = "SELECT id, email, password FROM users WHERE email=? AND password=?"
        cursor.execute(sql, (email, password))
        result = cursor.fetchall()
        return result
    

    except sqlite3.Error as e:
        print("Operation Error:",e)

    connection.commit()
    cursor.close()

# Get All users

def getAllUsers():
    try:
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    
    except sqlite3.Error as e:
        print("Operation Error:",e)   


#chat Exist
def get_room(user1_id, user2_id):
    query = """
        SELECT r.id
        FROM room r
        JOIN roomUser ru1 ON r.id = ru1.roomId
        JOIN roomUser ru2 ON r.id = ru2.roomId
        WHERE ru1.userId = ? AND ru2.userId = ?
    """
    cursor.execute(query, (user1_id, user2_id))
    room = cursor.fetchone()
    return room

def create_room(user1_id, user2_id):
    query = "INSERT INTO room (idType, time) VALUES (?, ?)"
    cursor.execute(query, (1, '2025-01-15 12:00:00'))  # idType=1 para "private"
    connection.commit()
    
    room_id = cursor.lastrowid  # Obtener el id de la sala recién creada
    
    # Agregar los usuarios a la sala
    query = "INSERT INTO roomUser (roomId, userId) VALUES (?, ?)"
    cursor.executemany(query, [(room_id, user1_id), (room_id, user2_id)])
    connection.commit()
    
    return room_id

def get_messages(room_id):
    # Obtener los mensajes de la base de datos para la sala específica
    cursor.execute("SELECT idUser, message, date FROM messages WHERE idRoom = ?", (room_id,))
    messages = cursor.fetchall()
    print(messages)
    return messages


def send_message(user_id, room_id, message, date):
    query = """
        INSERT INTO messages (idUser, idRoom, message, date)
        VALUES (?, ?, ?, ?)
    """
    cursor.execute(query, (user_id, room_id, message, date))
    connection.commit()

get_messages(1)

