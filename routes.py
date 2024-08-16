from app import app
from flask import render_template, redirect, request, session
import users, quizzes

@app.route("/")
def index():
	
	return(render_template("index.html"))

@app.route("/play")
def browse():
	
	session["game"] = 0
	quiz_list = quizzes.get_quiz_list()
	if quiz_list == False:
		return render_template("error.html", message="Visojen hakemisessa tapahtui virhe")
	
	return render_template("play.html", quiz_list=quiz_list)

@app.route("/play/", methods=["GET", "POST"])
def play():

	if request.method == "GET":
		if session.get("game",0) == 0:
			quizzes.create_game(request.args.get("quiz_id"), users.user_id())
		
		quiz = quizzes.get_quiz(request.args.get("quiz_id"))
		question = quizzes.get_question(quiz.id, quizzes.get_answer_count(session.get("game")) + 1)
	
		return render_template("quiz.html", quiz=quiz, question=question)
	
	if request.method == "POST":
		quiz_id = request.form["quiz_id"]
		question_id= request.form["question_id"]
		choice_id = request.form["choice"]

		if quizzes.add_answer(session.get("game"), question_id, choice_id):
			if quizzes.get_answer_count(session.get("game")) >= 5:
				return redirect("/result")
			else:
				quiz = quizzes.get_quiz(quiz_id)
				question = quizzes.get_question(quiz.id, quizzes.get_answer_count(session.get("game")) + 1)

				return render_template("quiz.html", quiz=quiz, question=question)
		else:
			return render_template("error.html", message="Vastauksen lisäämisessä tapahtui virhe")
	
@app.route("/result")
def result():

	results = quizzes.get_results(session.get("game"))
	answers = quizzes.get_answers(session.get("game"))

	return render_template("result.html", results=results, answers=answers)


@app.route("/review", methods=["POST"])
def review():

	quiz_id = request.form["quiz_id"]
	grade = request.form["grade"]
	comment = request.form["comment"]

	print(quiz_id)

	if quizzes.add_review(quiz_id, grade, comment):
		return redirect("/")
	else:
		return render_template("error.html", message="Tapahtui virhe arvostelun jättämisessä")

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

@app.route("/profile")
def profile():

	user = users.get_user_information(users.user_id())
	games = users.get_user_games(users.user_id())
	quizzes = users.get_user_quizzes(users.user_id())

	return render_template("profile.html", user=user, games=games, quizzes=quizzes)

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
