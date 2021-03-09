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
        cursor.execute("SELECT  users.id, users.email, users.username, users.bio, users.birthday from follow Inner join users on users.id = follow.user2_id where follow.user1_id = ?"[userId])
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




        def post():
            token = request.json.get("loginToken")
            followId = request.json.get("followId")
            affected_rows = None
            try:
                conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
                cursor = conn.cursor()
                cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
                user1_id = cursor.fetchall()[0][0]
                cursor.execute("INSERT INTO follow values (?,?)",[user1_id,followId])
                conn.commit()
                affected_rows = cursor.rowcount
            except Exception as ex :
                print("exception is : " + ex)  
            finally:
                if(conn != None):
                    conn.close()
                if (cursor != None):
                    cursor.close()
                if affected_rows == 1:
                    return Response("follow success",mimetype="html/text", status=204)
                else:
                    return Response("follow faliure", mimetype="html/text", status=400)              

        def delete():
            token = request.json.get("loginToken")
            followId = request.json.get("followId")
            affected_rows = None
            try:
                conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
                cursor = conn.cursor()
                cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
                user1_id = cursor.fetchall()[0][0]
                cursor.execute("DELETE FROM follow where useer1_id = ? and user2_id = ?",[user1_id,followId])
                conn.commit()
                affected_rows = cursor.rowcount
            except Exception as ex :
                print("exception is : " + ex)  
            finally:
                if(conn != None):
                    conn.close()
                if (cursor != None):
                    cursor.close()
                if affected_rows == 1:
                    return Response("delete follow success",mimetype="html/text", status=204)
                else:
                    return Response(" delete follow faliure", mimetype="html/text", status=400)              
