import mariadb
from flask import request, Response
import dbcreds
import json

def get():
    comment_id = request.args.get("commentId")
    users = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        if comment_id != None:
            cursor.execute("SELECT users.username, users.id, comment_like.comment_id from comment_like INNER JOIN users ON users.id = comment_like.user_id WHERE comment_like.comment_id = ?",[comment_id])
        else:
            cursor.execute("SELECT users.username, users.id, comment_like.comment_id from comment_like INNER JOIN users ON users.id = comment_like.user_id")  
        likes = cursor.fetchall()

    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close() 
        if likes != None:
            listOfLikes = []
            for like in likes:
                dic = {
                    "commentId": like[2],
                    "userId": like[1],
                    "username": like[0]
                }
                listOfLikes.append(dic)
            return Response(json.dumps(listOfLikes,default=str),mimetype="application/json",status=200)
        else:
            return Response("comment likes failed",mimetype="html/text",status=400)   

def post():
    token = request.json.get("loginToken")
    comment_id =request.json.get("commentId") 
    affected_rows = None
    like = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO comment_like (user_id,comment_id) VALUES (?,?)",[user_id,comment_id])
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.execute("SELECT users.username, users.id, comment_like.comment_id from comment_like INNER JOIN users ON user.id = comment_like.user_id WHERE comment_like.comment_id  = ?",[comment_id])
        likes = cursor.fetchall()[0]
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close() 
        if affected_rows == 1:
            dic = {
                "commentId": like[2],
                "userId": like [1],
                "username" : like [0]
            }
            return Response(json.dumps(dic),mimetype="application/json",status=201)
        else:
            return Response("comment like post failire", mimetype="html/text",status=400)    

def delete():
    token = request.json.get("loginToken")
    comment_id =request.json.get("commentId") 
    affected_rows = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("DELETE FROM comment_like where user_id =? and comment_id = ?",[user_id,comment_id])
        conn.commit()
        affected_rows = cursor.rowcount
    except Exception as ex:
        print(ex)
    finally:
        if(conn != None):
            conn.close()
        if (cursor != None):
            cursor.close() 
        if affected_rows == 1:
            return Response("comment like delete success",mimetype="html/text",status=204)
        else:
            return Response("comment like  delete failire", mimetype="html/text",status=400)   