from db import db
from flask import session
import users
from sqlalchemy.sql import text

def get_quiz_list():
	try:
		sql = text("SELECT q.id, u.nickname, q.name, q.category FROM quizzes q, users u WHERE u.id = q.creator_id ORDER BY q.id DESC;")
		quizzes = db.session.execute(sql).fetchall()
		db.session.commit()
	except:
		return False

	return quizzes

def get_quiz(quiz_id):
	try:
		sql = text("SELECT q.id, u.nickname, q.name, q.category FROM quizzes q, users u WHERE u.id = q.creator_id AND q.id = :quiz_id")
		quiz = db.session.execute(sql, {"quiz_id":quiz_id}).fetchone()
		db.session.commit()
	except:
		return False
	
	return quiz

def get_questions(quiz_id):
	try:
		sql = text("SELECT id, question FROM questions WHERE quiz_id = :quiz_id")
		questions = db.session.execute(sql, {"quiz_id":quiz_id}).fetchall()
		db.session.commit()
	except:
		return False
	
	return questions


def get_choices(question_id):
	try:
		sql = text("SELECT * FROM choices WHERE question_id = :question_id")
		choices = db.session.execute(sql, {"question_id":question_id}).fetchall()
		db.session.commit()

		for choice in choices:
			print(choice)
			print(choice.id, choice.question_id, choice.choice, choice.is_correct)

	except:
		return False
	
	return choices

def create(name, category):
	try:
		creator_id = users.user_id()
		sql = text("INSERT INTO quizzes (creator_id, name, category) VALUES (:creator_id,:name,:category) RETURNING id")
		result = db.session.execute(sql, {"creator_id":creator_id, "name":name, "category":category}).fetchone()
		db.session.commit()
	except:
		return False

	return result.id

def add_question(quiz_id, question, choices, answer):
	try:
		sql = text("INSERT INTO questions (quiz_id, question) VALUES (:quiz_id, :question) RETURNING id")
		result = db.session.execute(sql, {"quiz_id":quiz_id, "question":question}).fetchone()
		db.session.commit()

		question_id = result[0]

		for choice in choices:
			is_correct = False
			if choice == answer:
				is_correct = True
			
			print(choice, answer, is_correct)

			sql = text("INSERT INTO choices (question_id, choice, is_correct) VALUES (:question_id, :choice, :is_correct)")
			db.session.execute(sql, {"question_id":question_id, "choice":choice, "is_correct":is_correct})
			db.session.commit()

		sql = text("SELECT COUNT(*) FROM questions WHERE quiz_id=:quiz_id")
		count = db.session.execute(sql, {"quiz_id":quiz_id}).fetchone()
		db.session.commit()

	except:
		return False

	return count[0]
