from flask import Flask, request
import mariadb 
import dbcreds
import users
import login
import follows
import followers
import tweets
import tweetLikes
import comment_likes
import comments
import tweetLikes


from flask_cors import CORS 
app = Flask(__name__)
CORS(app)

@app.route("/api/user",methods=["GET", "POST", "PATCH", "DELETE"])
def getUsers():
    if request.method == "GET":
        return user.get_users()
    elif request.method == "POST":
        return user.post_user()  
    elif request.method == "PATCH":
        return user.patch_user()
    elif request.method == "DELETE":
        return user.delete_user()  
    else:
        Response("Not Supported", mimetype="text/html", status=500) 

@app.route("/api/login", methods=["POST", "DELETe"])
def user_login():
    if request.method == "POST":
        return login.post()
    elif request.method == "DELETE":
        return login.delete()
    else :
        Response("Not Supported", mimetype="text/hmtl", status=500) 

@app.route("/api/follows", methods=["GET", "POST", "DELETE"])
def follow_api():
    if request.method == "GET": 
        return follows.get()
    elif request.method == "POST":
         return follows.post()
    elif request.method == "DELETE":
         return follows.delete()
    else: 
        Response("Not Supported", mimetype="text/html", status=500)

@app.route("/api/followers", methods=["GET"])
def followers_api():
    if request.method == "GET":
        return followers.get()    
    else :
        Response("not supported", mimetype="text/html", status=500) 

@app.route("/api/tweets",methods=["GET","POST","PATCH","DELETE"])
def tweet():
    if request.method == "GET":
        return tweets.get()
    elif request.method=="POST":
        return tweets.post()
    elif request.method=="PATCH":
        return tweets.patch()
    elif request.method=="DELETE":
        return tweets.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/comments",methods=["GET","POST","PATCH","DELETE"])
def comment():
    if request.method == "GET":
        return comments.get()
    elif request.method=="POST":
        return comments.post()
    elif request.method=="PATCH":
        return comments.patch()
    elif request.method=="DELETE":
        return comments.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/tweet-likes",methods=["GET","POST","DELETE"])
def tweet_likes():
    if request.method == "GET":
        return tweetLikes.get()
    elif request.method=="POST":
        return tweetLikes.post()
    elif request.method=="DELETE":
        return tweetLikes.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)

@app.route("/api/comment-likes",methods=["GET","POST","DELETE"])
def commentLikes():
    if request.method == "GET":
        return comment_likes.get()
    elif request.method=="POST":
        return comment_likes.post()
    elif request.method=="DELETE":
        return comment_likes.delete()
    else :
        Response("not supported", mimetype="text/html", status=500)


