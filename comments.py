import mariadb
from flask import request, Response
import dbcreds
import json

def get():
    tweetId = request.args.get("tweetID")
    comment = None

    try: 
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        if tweetId != None :
            cursor.execute("SELECT comments.id, comments.tweet_id, comment.user_id, users.username, comments.content, comments.created_at FROM comments INNER JOIN users ON comments.user_id = users.id where comments.tweet_id = ?",[tweetId])
            comments = cursor.fetchall()
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if comments !=None :
            listOfcomments = []
            for comment in comments:
                dic = {
                    "commentId" : comment[0],
                    "tweetId" : comment[1],
                    "userId" : comment[2],
                    "username": comment[3],
                    "content" : comment[4],
                    "createdAt" : comment[5]
                }
                listOfcomments.append(dic)
            return Response(json.dumps(listOfcomments,default=str),mimetype="application/json",status=200)
        else:
            return Response("comments faliure",mimetype="html/text", status=400)

def post():
    token = request.json.get("loginToken")
    content = request.json.get("content")
    tweet_id = request.json.get("tweetId")
    user_id = None
    username =None
    createdAt = None
    comment_id = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",token)
        user_id = cursor.fetchall()[0][0]
        cursor.execute("SELECT username from users where id = ?",[user_id])
        username = cursor.fetchall()[0][0]
        cursor.execute("INSERT INTO comments (tweet_id,user_id,content) VALUES (?,?,?)",[tweet_id,user_id,content])
        conn.commit()
        comment_id = cursor.lastrowid
        cursor.execute("SELECT created_at from comments where  id = ?",[comment_id])
        createdAt = cursor.fetchall()[0][0]
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if comment_id !=None :
            dic = {
                "commentId" : comment_id,
                "tweetId" : tweet_id,
                "userId" : user_id,
                "username": username,
                "content" : content,
                "createdAt" : createdAt
            }
                
            return Response(json.dumps(dic,default=str),mimetype="application/json",status=201)
        else:
            return Response("comment post falied",mimetype="html/text", status=400)

def patch():
    token = request.json.get("loginToken")
    content = request.json.get("content")
    comment_id = request.json.get("commentId")
    affected_rows = None
    username = None
    comment = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("UPDATE comments SET content = ? WHERE id = ? and user_id = ?",[content, comment_id,user_id])
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.execute("SELECT username from users where id = ?",[user_id])
        username = cursor.fetchall()[0][0]
        cursor.execute("SELECT * FROM comments where id = ?",[comment_id])
        comment = cursor.fetchall()[0]
    except Exception as ex:
        print(ex)
    finally: 
        if(conn !=None):
            conn.close()
        if(cursor !=None):
            cursor.close()
        if affected_rows == 1 :
            dic = {
                "commentId" : comment_id,
                "tweetId" : comment[3],
                "userId" : user_id,
                "username": username,
                "content" : content,
                "createdAt" : comment[2]
            }
                
            return Response(json.dumps(dic,default=str),mimetype="application/json",status=201)
        else:
            return Response("comment patch falied",mimetype="html/text", status=400)            
       
def delete():
    token = request.json.get("loginToken")
    comment_id = request.json.get("commentId")
    affected_rows = None
    try:
        conn = mariadb.connect(user = dbcreds.username , port = dbcreds.port , host = dbcreds.host , password = dbcreds.password , database = dbcreds.database)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id from user_session where login_token = ?",[token])
        user_id = cursor.fetchall()[0][0]
        cursor.execute("DELETE from comments WHERE id = ? and user_id = ?",[comment_id,user_id])
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
            return Response("comment delete falied",mimetype="html/text", status=400)            
       
