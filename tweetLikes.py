import mariadb
from flask import request, Response
import dbcreds
import json

def get():
    tweet_id = request.args.get("tweetId")
    users = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        if tweet_id != None:
            cursor.execute("SELECT users.username, users.id, tweet_like.tweet_id from tweet_like INNER JOIN users ON users.id = tweet_like.user_id WHERE tweet_like.tweet_id = ?",[tweet_id])
        else:
            cursor.execute("SELECT users.username, users.id, tweet_like.tweet_id from tweet_like INNER JOIN users ON users.id = tweet_like.user_id")  
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
                    "tweetId": like[2],
                    "userId": like[1],
                    "username": like[0]
                }
                listOfLikes.append(dic)
            return Response(json.dumps(listOfLikes,default=str),mimetype="application/json",status=200)
        else:
            return Response("tweet likes failed",mimetype="html/text",status=400)   

def post():
    token = request.json.get("loginToken")
    tweet_id = request.json.get("tweetId") 
    affected_rows = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO tweet_like (user_id,tweet_id) VALUES (?,?)",[user_id,tweet_id])
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
            return Response("like success",mimetype="html/text",status=201)
        else:
            return Response("like failire", mimetype="html/text",status=400)    

def delete():
    token = request.json.get("loginToken")
    tweet_id =request.json.get("tweetId") 
    affected_rows = None

    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("DELETE FROM tweet_like where user_id =? and tweet_id = ?",[user_id,tweet_id])
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
            return Response("like delete success",mimetype="html/text",status=204)
        else:
            return Response("like  delete failiure", mimetype="html/text",status=400)            

                                         