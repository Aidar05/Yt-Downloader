from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from extractor import extractVideoData
from filter_formats import filterFormats
from db_logic import *
import mysql.connector

app = Flask(__name__)
app.secret_key = 'eaa2cc52a16507cf194e4f0c'

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="ytdownloader_data"
)

@app.route('/')
def main_page():
  print(session)

  if 'logged_in' in session:
    get_user_data(db, session['user_id'])

    print(session)
    return render_template(
      'index-logged-in.html',
      )
  else:
    return render_template('index.html')
  
@app.route('/download', methods=["POST"])
def download():
  videoUrl = request.form["video_url"]
  videoData = extractVideoData(videoUrl)
  title = videoData["title"]
  formats = filterFormats(videoData["formats"])
  thumbnail = videoData["thumbnail"]
  user_id = session["user_id"]
  save_to_history(db, videoUrl, user_id)

  return render_template(
    'download.html',
    title=title,
    formats=formats,
    thumbnail=thumbnail
  )

@app.route('/profile', methods=["POST", "GET"])
def get_profile_info():
  return render_template('profile.html')

@app.route('/sign-up', methods=['POST', 'GET'])
def registration():
  if request.method == "GET":
    return render_template("sign-up.html")
  
  elif request.method == "POST":
    username = request.form["username"]
    email = request.form["email"]
    password = request.form['password']
    add_user(db, username, email, password)

    add_userData_toSession(username)

    return redirect(url_for("main_page"))

@app.route('/sign-in', methods=['POST', 'GET'])
def login():
  if request.method == "GET":
    return render_template("sign-in.html")
  
  elif request.method == "POST":
    # Может быть либо именем либо почтой
    username = request.form["login"]  
    password = request.form['password']   
    
    if check_user(db, username, password)[0]:
      add_userData_toSession(username)
      return redirect(url_for("main_page"))
    else: 
      return render_template("sign-in.html")

@app.route('/log-out')
def logout():
  session.clear()
  return redirect(url_for('main_page'))

def add_userData_toSession(login):
  session['user_id'] = get_user_id(db, login)
  user_data = get_user_data(db, session['user_id'])
  
  session['logged_in'] = True
  session['username'] = user_data[1]
  session['email'] = user_data[2]

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='43345', debug=True)