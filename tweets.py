import mariadb
from flask import request, Response
import dbcreds
import json

def get():
    userId = request.args.get("userId")
    tweets = None

    try: 
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        if userId != None :
            cursor.execute("SELECT tweets.id, tweets.user_id, users.username, tweets.content, tweets.created_at FROM tweets INNER JOIN users ON tweets.user_id = users.id where tweets.user_id = ?",[userId])
            tweets = cursor.fetchall()
        else:
            cursor.execute("SELECT tweets.id, tweets.user_id, users.username, tweets.content, tweets.created_at FROM tweets INNER JOIN users ON tweets.user_id = users.id")
            tweets = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if tweets !=None :
            listOfTweets = []
            for tweet in tweets:
                dic = {
                    "tweetId" : tweet[0],
                    "userId" : tweet[1],
                    "username": tweet[2],
                    "content" : tweet[3],
                    "createdAt" : tweet[4]
                }
                listOfTweets.append(dic)
            return Response(json.dumps(listOfTweets,default=str),mimetype="application/json",status=200)
        else:
            return Response("tweets faliure",mimetype="html/text", status=400)

def post():
    token = request.json.get("loginToken")
    content = request.json.get("content")
    user_id = None
    username =None
    tweet_id = None
    createdAt = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("SELECT username from users where id = ?",[user_id])
        username = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO tweets (user_id,content) VALUES (?,?)",[user_id,content])
        conn.commit()
        tweet_id = cursor.lastrowid
        cursor.execute("SELECT created_at from tweets where  id = ?",[tweet_id])
        createdAt = cursor.fetchall()[0][0]
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if tweet_id !=None :
            dic = {
                "tweetId" : tweet_id,
                "userId" : user_id,
                "username": username,
                "content" : content,
                "createdAt" : createdAt
            }
                
            return Response(json.dumps(dic,default=str),mimetype="application/json",status=201)
        else:
            return Response("tweets post faliure",mimetype="html/text", status=400)

def patch():
    token = request.json.get("loginToken")
    content = request.json.get("content")
    tweet_id = request.json.get("tweetId")
    affected_rows = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("UPDATE tweets SET content = ? WHERE id = ? and user_id = ?",[content, tweet_id,user_id])
        conn.commit()
        affected_rows = cursor.rowcount
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if affected_rows == 1 :
            dic = {
                "tweetId" : tweet_id,
                "content" : content,
               
            }
                
            return Response(json.dumps(dic,default=str),mimetype="application/json",status=201)
        else:
            return Response("tweets patch falied",mimetype="html/text", status=400)            
       
def delete():
    token = request.json.get("loginToken")
    tweet_id = request.json.get("tweetId")
    affected_rows = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("DELETE from tweets WHERE id = ? and user_id = ?",[tweet_id,user_id])
        conn.commit()
        affected_rows = cursor.rowcount
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if affected_rows == 1 :
            return Response("delete success",mimetype="application/json",status=204)
        else:
            return Response("tweets delete falied",mimetype="html/text", status=400)            
       
