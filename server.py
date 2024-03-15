from flask import Flask, render_template, request, session, redirect, url_for
from extractor import extractVideoData
from filter_formats import filterFormats
from db_logic import add_user, check_user 

app = Flask(__name__)
app.secret_key = 'eaa2cc52a16507cf194e4f0c'

@app.route('/')
def main_page():
  if 'username' in session:
    return render_template('index-logged-in.html', username=session['username'])
  else:
    return render_template('index.html')
  
@app.route('/download', methods=["POST"])
def download():
  videoUrl = request.form["video_url"]
  videoData = extractVideoData(videoUrl)

  title = videoData["title"]
  formats = filterFormats(videoData["formats"])
  thumbnail = videoData["thumbnail"]

  return render_template(
    'download.html',
    title=title,
    formats=formats,
    thumbnail=thumbnail
  )

@app.route('/sign-up', methods=['POST', 'GET'])
def registration():
  if request.method == "GET":
    return render_template("sign-up.html")
  
  elif request.method == "POST":
    username = request.form["username"]
    email = request.form["email"]
    password = request.form['password']
    add_user(username, email, password)

    session['username'] = username  
    return redirect(url_for("main_page"))

@app.route('/sign-in', methods=['POST', 'GET'])
def login():
  if request.method == "GET":
    return render_template("sign-in.html")
  
  elif request.method == "POST":
    username = request.form["login"]
    password = request.form['password']   

    if check_user(username, password):
      session['username'] = username  
    
    return redirect(url_for("main_page"))


if __name__ == '__main__':
  app.run(host='0.0.0.0', port='43345', debug=True)