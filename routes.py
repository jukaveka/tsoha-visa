from app import app
from flask import render_template, redirect, request, session, abort
import users, quizzes

@app.route("/")
def index():
	
	return(render_template("index.html"))

@app.route("/browse")
def browse():
	
	session["game"] = 0
	page = request.args.get('page', 1, type=int)
	quiz_list = quizzes.get_quiz_list()

	if quiz_list == False:
		
		return render_template("error.html", message="Visojen hakemisessa tapahtui virhe")

	result = quizzes.get_page_items(page, quiz_list)
	items = result[0]
	total_pages = result[1]
	
	return render_template("browse.html", quizzes=items, page=page, total_pages=total_pages)

@app.route("/play/", methods=["GET", "POST"])
def play():

	if request.method == "GET":
		
		if session.get("game",0) == 0:
			
			quizzes.create_game(request.args.get("quiz_id"), users.user_id())
		
		quiz = quizzes.get_quiz(request.args.get("quiz_id"))
		question = quizzes.get_question(quiz.id, quizzes.get_answer_count(session.get("game")) + 1)
		choices = quizzes.get_choices(quiz.id, quizzes.get_answer_count(session.get("game")) + 1)
	
		return render_template("quiz.html", quiz=quiz, question=question, choices=choices)
	
	if request.method == "POST":

		if users.check_csrf_token(request.form["csrf_token"]):
		
			quiz_id = request.form["quiz_id"]
			question_id= request.form["question_id"]
			choice_id = request.form["choice"]

			if quizzes.add_answer(session.get("game"), question_id, choice_id):

				if quizzes.get_answer_count(session.get("game")) >= 5:

					return redirect("/result")

				else:

					quiz = quizzes.get_quiz(quiz_id)
					question = quizzes.get_question(quiz.id, quizzes.get_answer_count(session.get("game")) + 1)
					choices = quizzes.get_choices(quiz.id, quizzes.get_answer_count(session.get("game")) + 1)

					return render_template("quiz.html", quiz=quiz, question=question, choices=choices)
			else:

				return render_template("error.html", message="Vastauksen lisäämisessä tapahtui virhe")
		
		else:

			abort(403)

# Quitting games
@app.route("/quit")
def quit():

	game_id = session.get("game", 0)

	if quizzes.quit_game(game_id):
		return redirect("/browse")
	else:
		return render_template("error.html", message="Virhe pelin lopettamisessa")
	
# Stppping quiz creation
@app.route("/stop")
def stop():

	quiz_id = request.args.get("quiz_id")

	if quizzes.stop_quiz_creation(quiz_id):
		return redirect("/")
	else:
		return render_template("error.html", message="Virhe visan luonnin lopettamisessa")
		
@app.route("/play/reviews/")
def reviews():
	
	quiz_id = request.args.get("quiz_id")
	quiz = quizzes.get_quiz(quiz_id)
	review_list = quizzes.get_quiz_reviews(quiz_id)

	print(review_list)

	if review_list == False:
		
		return render_template("error.html", message="Arvostelujen hakemisessa tapahtui virhe")

	page = request.args.get('page', 1, type=int)
	result = quizzes.get_page_items(page, review_list)
	reviews=result[0]
	total_pages = result[1]

	return render_template("reviews.html", quiz=quiz, reviews=reviews, page=page, total_pages=total_pages)
	
@app.route("/result")
def result():

	results = quizzes.get_results(session.get("game"))
	answers = quizzes.get_answers(session.get("game"))

	return render_template("result.html", results=results, answers=answers)

@app.route("/review", methods=["GET", "POST"])
def review():

	if request.method == "GET":

		return render_template("review.html")

	if request.method == "POST":

		if users.check_csrf_token(request.form["csrf_token"]):

			game_id = session.get("game", 0)
			grade = request.form["grade"]
			comment = request.form["comment"]

			if quizzes.add_review(game_id, grade, comment):

				return redirect("/")

			else:

				return render_template("error.html", message="Tapahtui virhe arvostelun jättämisessä")

		else:

			abort(403)

@app.route("/new")
def new():
	
	return(render_template("new.html"))

@app.route("/create", methods=["POST"])
def create():

	if users.check_csrf_token(request.form["csrf_token"]):
	
		name = request.form["name"]
		category = request.form["category"]
		quiz = quizzes.create_quiz(name, category)

		if quiz.id != False:

			return render_template("question.html", quiz_id=quiz.id)

		else:

			return render_template("error.html", message="Visan luonti epäonnistui.")
	
	else:
		
		abort(403)

@app.route("/create/question", methods=["GET", "POST"])
def create_question():
	
	if request.method == "GET":
		
		return render_template("question.html")
	
	if request.method == "POST" and users.check_csrf_token(request.form["csrf_token"]):
		
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
	
	else:
		
		abort(403)

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
