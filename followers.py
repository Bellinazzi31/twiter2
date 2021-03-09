import mariadb
from flask import request, Response
import dbcreds
import json

def get():
    userId = request.args.get("userId")
    users = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT  users.id, users.email, users.username, users.bio, users.birthday from follow Inner join users on users.id = follow.user1_id where follow.user2_id = ?"[userId])
        users = cursor.fetchall()
    except Exception as ex :
        print("exception is : " + ex)    
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close()
        if users != None:
            listofUsers = []
            for item in users :
                dic = {
                    "userId": userId[0],
                    "email": user[1],
                    "username": user[2],
                    "bio": user[3],
                    "birthday": user[4]
                }
                listofUsers.append(dic)
            return Response (json.dumps(listofUsers,default=str),mimetype="application/json",status=200)
        else:
            return Response("bad request",mimetype="html/text",status=400)     



