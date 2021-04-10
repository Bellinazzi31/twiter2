import mariadb
from flask import request, Response
import dbcreds
import json
import secrets

def get_users():
    user_id = request.args.get("userId")
    users = None
    conn = None
    cursor = None

    try: 
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        if user_id !=None:
            cursor.execute("SELECT id, email, username, bio, birthday from users WHERE id = ?",[user_id])
        else:
            cursor.execute("SELECT id, email, username, bio, birthday from users" )
        users = cursor.fetchall()
    except Exception as e :
        print(e)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if users != None or users == []:
            listofUsers = []
            for item in users :
                dic = {
                    "userId": item [0],
                    "email" : item [1],
                    "username" : item [2],
                    "bio" : item[3],
                    "birthday" : item [4]
                }
                listofUsers.append(dic) 
            return Response(json.dumps(listofUsers,default=str),mimetype="application/json",status=200)
        return Response("bad request",mimetype="html/text",status=400)

def post_user():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    bio = request.json.get("bio")
    birthday = request.json.get("birthday")
    affected_rows = None
    userId = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username,email,,password,bio,birthday) Values(?,?,?,?,?)", [username,email,password,bio,birthday])
        conn.commit()
        userId = cursor.lastrowid
        token = secrets.token_urlsafe(24)
        cursor.execute("INSERT INTO user_session VALUES (?,?)", [userId,token])
        conn.commir()
        affected_rows = cursor.rowcount
    except Exception as ex :
        print("exception is :" + ex )  
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if affected_rows == 1:
            user = {
                "userId": userId,
                "email": email,
                "username": username,
                "bio": bio,
                "birthday": birthday,
                "logintoken": token
            }
            return Response (json.dumps(user,default=str),mimetype="application/json",status=201)
        else:
            return Response("user insert failed",mimetype="html/text",status=400)    
             

def patch_user():
    token = request.json.get("loginToken")
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")
    bio = request.json.get("bio")
    birthday = request.json.get("birthday")
    affected_rows = None
    userId = None
    user = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_session WHERE login_token = ?", [token])
        userId = cursor.fetchall()[0][0]
        if username != None :
            cursor.execute("UPDATE users SET username = ? Where id = ?",[username,userId])
        if email != None :
            cursor.execute("UPDATE users SET email = ?",[email,userId])
        if password != None :
            cursor.execute("UPDATE users SET password = ?",[password,userId])
        if bio != None :
            cursor.execute("UPDATE users SET bio = ?",[bio,userId]) 
        if birthday != None :
            cursor.execute("UPDATE users SET birthday = ?",[birthday,userId])               
        conn.commir()
        affected_rows = cursor.rowcount
        cursor.execute("SELECT id, email, username, bio, birthday from users WHERE id =?",[userId])
        user = cursor.fetchall()[0]
    except Exception as ex :
        print("exception is :" + ex )  
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if affected_rows == 1:
            user = {
                "userId": userId[0],
                "email": user[1],
                "username": user[2],
                "bio": user[3],
                "birthday": user[4]
            }
            return Response (json.dumps(user,default=str),mimetype="application/json",status=200)
        else:
            return Response("user patch failed",mimetype="html/text",status=400) 

def delete_user():  
    token = request.json.get("loginToken")
    password = request.json.get("password")
    affected_rows = None 
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_session WHERE login_token = ?", [token])
        userId = cursor.fetchall()[0][0]
        cursor.execute("SELECT password FROM users where id =? ", [userId])
        user_password = cursor.fetchall()[0][0]
        if(password == user_password):
            cursor.execute("DELETE FROM users where id = ?", [userId])
            conn.commit()
            affected_rows = cursor.rowcount
    except Exception as ex :
        print("exception is :" + ex )  
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if affected_rows == 1:
            return Response ("user delete success",mimetype="html/text",status=204)
        else:
            return Response("user delete failed",mimetype="html/text",status=400)    
                                                