from app import app
from flask import render_template, redirect, request
import users, quizzes

@app.route("/")
def index():
	return(render_template("index.html"))

@app.route("/play")
def browse():
	quiz_list = quizzes.get_quiz_list()
	return render_template("play.html", quiz_list=quiz_list)

@app.route("/play/", methods=["GET", "POST"])
def play():
	if request.method == "GET":
		game = quizzes.create_game(request.args.get("quiz_id"), users.user_id())
		quiz = quizzes.get_quiz(request.args.get("quiz_id"))
		question = quizzes.get_question(quiz.id, 1)
	
		return render_template("quiz.html", quiz=quiz, question=question, game=game)
	
	if request.method == "POST":
		return redirect("/") # Tästä jatkuu

@app.route("/new")
def new():
	return(render_template("new.html"))

@app.route("/create", methods=["POST"])
def create():
	name = request.form["name"]
	category = request.form["category"]
	quiz = quizzes.create_quiz(name, category)
	if quiz.id != False:
		return render_template("question.html", quiz_id=quiz.id)
	else:
		return render_template("error.html", message="Visan luonti epäonnistui.")

@app.route("/create/question", methods=["GET", "POST"])
def create_question():
	if request.method == "GET":
		return render_template("question.html")
	if request.method == "POST":
		quiz_id = request.form["quiz_id"]
		question = request.form["question"]
		choice1 = request.form["choice1"]
		choice2 = request.form["choice2"]
		choice3 = request.form["choice3"]
		choice4 = request.form["choice4"]
		choices = [choice1, choice2, choice3, choice4]
		correct_choice = request.form["correct_choice"]
		answer = request.form[correct_choice]

		count = quizzes.add_question(quiz_id, question, choices, answer)

		if count >= 5: # Currently forcing 5 questions per quiz
			return redirect("/")
		else:
			return render_template("question.html", quiz_id=quiz_id)

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
