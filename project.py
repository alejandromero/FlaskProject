from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from hashlib import sha256 #generate and see str, sha(str).hexdigext()
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Users(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), unique = True, nullable = False) 
	password = db.Column(db.String(80), nullable = False)

@app.route('/')
@app.route('/main')
def main():
	return render_template("main.html")

@app.route('/browser')
def browser():
		return render_template("browser.html")

@app.route('/search')
def search():
	filename = request.args.get("filename") 
	if os.path.isfile("files/public/"+str(filename)):
		return render_template("results.html", results = "File found", origin = "browser")
	else:
		return render_template("results.html", results = "File not found", origin = "browser")

@app.route('/login', methods = ["GET","POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(username = request.form["username"]).first()
		
		if user and user.password==sha256(request.form["password"]).hexdigext(): 
			return "You're logged in"
		else:
			return "Check you're password and try again"
	return render_template("login.html")
	
@app.route('/signup', methods = ["POST", "GET"])
def signup():
	if request.method == "POST":
		username = request.form["username"]
		hasehd_password = sha256(request.form["password"]).hexdigest()
		new_user = Users(username = username, password = hasehd_password) 
		db.session.add(new_user)
		db.session.commit()
	return render_template("signup.html")


if __name__=="__main__":
	db.create_all()
	for direc in ["files","files/public", "files/private"]:
		if os.path.isdir(direc):
			pass
		else:
			os.makedirs(direc)
	app.run(debug=True)