from db import db
from flask import session
import users
from sqlalchemy.sql import text

def get_quiz_list():

	try:
		sql = text("SELECT q.id, u.nickname, q.name, q.category FROM quizzes q, users u WHERE u.id = q.creator_id ORDER BY q.id DESC;")
		result = db.session.execute(sql)
		quizzes = result.fetchall()
		db.session.commit()
	except:
		return False

	return quizzes

def get_quiz(quiz_id):

	try:
		sql = text("SELECT q.id, u.nickname, q.name, q.category FROM quizzes q, users u WHERE u.id = q.creator_id AND q.id = :quiz_id")
		result = db.session.execute(sql, {"quiz_id":quiz_id})
		quiz = result.fetchone()
		db.session.commit()
	except:
		return False
	
	return quiz

def get_question(quiz_id, question_number):

	try:
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
	except:
		return False
	
	return question

def create_game(quiz_id, user_id):

	try:
		sql = text("INSERT INTO games (user_id, quiz_id) VALUES (:user_id, :quiz_id) RETURNING id")
		result = db.session.execute(sql, {"user_id":user_id, "quiz_id":quiz_id})
		game = result.fetchone()
		db.session.commit()
	except:
		return False
	
	return game

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

def get_question_count(quiz_id):

	try:
		sql = text("SELECT COUNT(*) AS question_count FROM questions WHERE quiz_id=:quiz_id")
		result = db.session.execute(sql, {"quiz_id":quiz_id})
		question = result.fetchone()
		print(question.question_count)
		db.session.commit()
	except:
		return False
	
	return question.question_count