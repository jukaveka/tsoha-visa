from db import db
from flask import session
import users
from sqlalchemy.sql import text

def create(name, category):
	try:
		sql = text("INSERT INTO quizzes (name, category) VALUES (:name,:category)")
		db.session.execute(sql, {"name":name, "category":category})
		db.session.commit()
	except:
		return False
	return True

def add_question(quiz_id, question, choices, answer):
	try:
		sql = text("INSERT INTO questions (quiz_id, question) VALUES (:quiz_id, :question))")
		db.session.execute(sql, {"quiz_id":quiz_id, "question":question})
		db.session.commit()
		
		sql = text("INSERT INTO choices (question_id, choice, is_correct) VALUES (:question_id, :choice, :is_correct))")
		db.session.execute(sql, {"question_id":question_id, "choice":choice, "is_correct":answer})
		db.session.commit()
	except:
		return False
	
	return True
