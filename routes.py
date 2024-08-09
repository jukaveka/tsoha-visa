from app import app
from flask import render_template, redirect, request
import users #, quizzes

@app.route("/")
def index():
	return(render_template("index.html"))

"""
@app.route("/quizzes")
def quizzes():
"""

@app.route("/new", methods=["GET", "POST"])
def new():
	if request.method == "POST":
		return 0
	else:
		return(render_template("new.html"))

"""
@app.route("/quizzes/<int:id>")
def quiz():
"""

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")
	if request.method == "POST":
		username = request.form["username"]
		password1 = request.form["password1"]
		password2 = request.form["password2"]
		if password1 != password2:
			return render_template("error.html", message="Salasanat eroavat")
		if users.register(username, password1):
			return redirect("/")
		else:
			return render_template("error.html", message="Tunnusten luonti epäonnistui")

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		return render_template("login.html")
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]
		if users.login(username, password):
			return redirect("/")
		else:
			return render_template("error.html", message="Kirjautuminen epäonnistui. Tarkista antamasi käyttäjätunnus tai salasana, ja yritä uudestaan")

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")
