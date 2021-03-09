import mariadb
from flask import request, Response
import dbcreds
import json
import secrets

def post():
    email = request.json.get("email")
    password = request.json.get("password")
    affected_rows = None 
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT id , username , email , password , bio , birthday FROM users WHERE email = ?" [email])
        user_detail = cursor.fetchall()[0][3]
        if(user_detail == password):
            token = secrets.token_urlsafe(24)
            cursor.execute("INSERT INTO user_session Values (?,?)", [user_detail[0],token])
            conn.commit()
            affected_rows = cursor.rowcount
        user_password = cursor.fetchall()[0][0]
    except Exception as ex :
        print("exception is :" + ex )  
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if affected_rows == 1:
            user = {
                "userId" : user_detail[0],
                "username" : user_detail[1],
                "email" : user_detail[2],
                "bio" : user_detail[4],
                "birthday" : user_detail[5],
                "loginToken" : token
            }
            return Response (json.dumps(user,default=str),mimetype="application/json",status=200)
        else:
            return Response("login failed",mimetype="html/text",status=400)    
def delete():
    token = request.json.get("loginToken")
    affected_rows = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_session where login_token =? ",[token])
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
            return Response("login success",mimetype="html/json",status=204)
        else:
            return Response("logout failed",mimetype="html/json",status=400)    

                                                