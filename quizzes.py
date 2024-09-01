from db import db
from flask import session
import users
from sqlalchemy.sql import text

def get_quiz_list():

	try:
		sql = text(
			"SELECT "
			    "q.id, "
			    "u.nickname, "
			    "q.name, "
			    "q.category, "
			    "COUNT(g.id) AS games_played, "
			    "COALESCE(CAST(SUM(r.grade) AS DOUBLE PRECISION)/ COUNT(r.id), 0) AS rating "
			"FROM "
			    "quizzes q "
			"INNER JOIN users u "
			    "ON u.id = q.creator_id "
			"LEFT JOIN games g "
			    "ON g.quiz_id = q.id "
			"LEFT JOIN reviews r "
			    "ON r.quiz_id = q.id "
			"GROUP BY "
			    "q.id, "
			    "u.nickname, "
			    "q.name, "
			    "q.category "
			"ORDER BY "
			    "q.id DESC; "
		)
		result = db.session.execute(sql)
		quizzes = result.fetchall()
		db.session.commit()
	except:
		return False

	return quizzes

def get_page_items(current_page, item_list):

	items_per_page = 5
	start_item = (current_page - 1) * items_per_page
	end_item = start_item + items_per_page
	total_pages = len(item_list) // items_per_page
	displayed_items = item_list[start_item:end_item]

	print(displayed_items)

	return displayed_items, total_pages

def get_quiz(quiz_id):

	try:
		sql = text("SELECT q.id, u.nickname, q.name, q.category FROM quizzes q, users u WHERE u.id = q.creator_id AND q.id = :quiz_id")
		result = db.session.execute(sql, {"quiz_id":quiz_id})
		quiz = result.fetchone()
		db.session.commit()
	except:
		return False
	
	return quiz

def get_quiz_reviews(quiz_id):

	sql = text("SELECT u.nickname AS reviewer, r.grade, r.comment FROM reviews AS r, users AS u WHERE u.id = r.user_id AND r.quiz_id = :quiz_id")
	result = db.session.execute(sql, {"quiz_id":quiz_id})
	reviews = result.fetchall()

	return reviews

def get_question(quiz_id, question_number):

	sql = text(
		"SELECT "
		    "q.id, " 
		    "q.question, "
		    "c1.id AS choice_1_id, "
		    "c1.choice AS choice_1, "
		    "c2.id AS choice_2_id, "
		    "c2.choice AS choice_2, "
		    "c3.id AS choice_3_id, "
		    "c3.choice AS choice_3, "
		    "c4.id AS choice_4_id, "
		    "c4.choice AS choice_4 "
		"FROM " 
		    "questions q, choices c1, choices c2, choices c3, choices c4, choices cc "
		"WHERE "
		    "q.id = c1.question_id AND c1.choice_number = 1 "
		    "AND q.id = c2.question_id AND c2.choice_number = 2 "
		    "AND q.id = c3.question_id AND c3.choice_number = 3 "
		    "AND q.id = c4.question_id AND c4.choice_number = 4 "
		    "AND q.id = cc.question_id AND cc.is_correct = True "
		    "AND q.quiz_id = :quiz_id "
			"AND q.question_number = :question_number"
	)
	result = db.session.execute(sql, {"quiz_id":quiz_id, "question_number":question_number})
	question = result.fetchone()
	db.session.commit()

	return question

def get_choices(quiz_id, question_number):

	sql = text("SELECT choice.id, choice.choice FROM choices AS choice, questions AS question WHERE choice.question_id = question.id AND question.quiz_id = :quiz_id AND question.question_number = :question_number")
	result = db.session.execute(sql, {"quiz_id":quiz_id, "question_number":question_number})
	choices = result.fetchall()

	return choices

def get_results(game_id):

	sql = text(
		"SELECT "
			"q.id AS quiz_id, "
		    "q.name AS quiz_name, "
		    "COUNT(*) AS correct_answer_count, "
		    "CAST((CAST(COUNT(*) AS DOUBLE PRECISION) / CAST(5 AS DOUBLE PRECISION)) * 100 AS INTEGER) AS correct_answer_percent "
		"FROM "
		    "games g, quizzes q, answers a "
		"WHERE "
		    "g.quiz_id = q.id "
		    "AND g.id = a.game_id "
		    "AND a.is_correct = True "
		    "AND g.id = :game_id "
		"GROUP BY "
			"q.id, "
		    "q.name "
	)
	result = db.session.execute(sql, {"game_id":game_id})
	results = result.fetchone()
	db.session.commit()

	return results

def get_answers(game_id):
	
	sql = text(
		"SELECT "
		    "q.question, "
		    "uc.choice AS user_answer, "
		    "cc.choice AS correct_answer, "
		    "CASE "
		        "WHEN a.is_correct = True THEN 'oikein' "
		        "ELSE 'väärin' "
		    "END AS was_user_correct "
		"FROM "
		    "answers a "
		"INNER JOIN questions AS q ON "
		    "q.id = a.question_id "
		"INNER JOIN choices AS uc ON "
		    "uc.id = a.choice_id "
		"INNER JOIN choices AS cc ON "
		    "cc.question_id = q.id "
		    "AND cc.is_correct = True "
		"WHERE "
		    "a.game_id = :game_id;"
	)
	result = db.session.execute(sql, {"game_id":game_id})
	answers = result.fetchall()
	db.session.commit()

	return answers

def create_game(quiz_id, user_id):

	try:
		sql = text("INSERT INTO games (user_id, quiz_id) VALUES (:user_id, :quiz_id) RETURNING id")
		result = db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id})
		game = result.fetchone()
		db.session.commit()
	except:
		return False
	
	session["game"] = game.id

	return game

def quit_game(game_id):

	try:
		sql = text("DELETE FROM answers WHERE game_id = :game_id")
		db.session.execute(sql, {"game_id":game_id})
		db.session.commit()
	except:
		return False

	try:
		sql = text("DELETE FROM games WHERE id = :game_id")
		db.session.execute(sql, {"game_id":game_id})
		db.session.commit()
	except:
		return False
	
	return True

def create_quiz(name, category):

	try:
		creator_id = users.user_id()
		sql = text("INSERT INTO quizzes (creator_id, name, category) VALUES (:creator_id,:name,:category) RETURNING id")
		result = db.session.execute(sql, {"creator_id":creator_id, "name":name, "category":category})
		quiz = result.fetchone()
		db.session.commit()
	except:
		return False

	return quiz

def add_question(quiz_id, question, choices, answer):

	question_number = get_question_count(quiz_id) + 1
	
	try:
		sql = text("INSERT INTO questions (quiz_id, question_number, question) VALUES (:quiz_id, :question_number, :question) RETURNING id")
		result = db.session.execute(sql, {"quiz_id":quiz_id, "question_number":question_number, "question":question})
		question = result.fetchone()
		db.session.commit()
	except:
		return False
	
	if add_choices(question.id, choices, answer):
		return get_question_count(quiz_id)
	else:
		return False 
	
def add_choices(question_id, choices, answer):

	choice_number = 1

	for choice in choices:
		is_correct = False
		if choice == answer:
			is_correct = True

		try:
			sql = text("INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (:question_id, :choice_number, :choice, :is_correct)")
			db.session.execute(sql, {"question_id":question_id, "choice_number":choice_number, "choice":choice, "is_correct":is_correct})
			db.session.commit()
			choice_number += 1
		except:
			return False

	return True

def add_answer(game_id, question_id, choice_id):

	is_correct = validate_answer(question_id, choice_id)

	try:
		sql = text("INSERT INTO answers (game_id, question_id, choice_id, is_correct) VALUES (:game_id, :question_id, :choice_id, :is_correct)")
		db.session.execute(sql, {"game_id":game_id,"question_id":question_id, "choice_id":choice_id, "is_correct":is_correct})
		db.session.commit()
	except:
		return False

	return True

def add_review(game_id, grade, comment):

	quiz_id = get_game_quiz(game_id)

	try:
		sql = text("INSERT INTO reviews (quiz_id, user_id, grade, comment) VALUES (:quiz_id, :user_id, :grade, :comment)")
		db.session.execute(sql, {"quiz_id":quiz_id, "user_id":users.user_id(), "grade":grade, "comment":comment})
		db.session.commit()
	except:
		return False
	
	return True

def get_game_quiz(game_id):
	
	sql = text("SELECT quiz_id FROM games WHERE id = :game_id")
	result = db.session.execute(sql, {"game_id":game_id})
	game = result.fetchone()

	return game.quiz_id

def validate_answer(question_id, id):
	
	sql = text("SELECT is_correct FROM choices WHERE question_id = :question_id AND id = :id")
	result = db.session.execute(sql, {"question_id":question_id, "id":id})
	choice = result.fetchone()
	
	return choice.is_correct

def get_question_count(quiz_id):

	sql = text("SELECT COUNT(*) AS question_count FROM questions WHERE quiz_id=:quiz_id")
	result = db.session.execute(sql, {"quiz_id":quiz_id})
	question = result.fetchone()
	db.session.commit()

	return question.question_count

def get_answer_count(game_id):

	sql = text("SELECT COUNT(*) AS answer_count FROM answers WHERE game_id = :game_id")
	result = db.session.execute(sql, {"game_id":game_id})
	answers = result.fetchone()
	db.session.commit()

	return answers.answer_count