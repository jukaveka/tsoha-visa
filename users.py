from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text


def login(username, password):
	sql = text("SELECT id, nickname, password FROM users WHERE nickname=:username")
	result = db.session.execute(sql, {"username":username})
	user = result.fetchone()
	if not user:
		return False
	else:
		if check_password_hash(user.password, password):
			session["user_id"] = user.id
			return True
		else:
			return False

def logout():
	del session["user_id"]

def register(username, password):
	hash_value = generate_password_hash(password)
	try:
		sql = text("INSERT INTO users (nickname,password) VALUES (:username,:password)")
		db.session.execute(sql, {"username":username, "password":hash_value})
		db.session.commit()
	except:
		return False
	return login(username, password)

def user_id():
	return session.get("user_id",0)

def get_user_information(user_id):

	sql = text("SELECT nickname FROM users WHERE id = :user_id")
	result = db.session.execute(sql, {"user_id":user_id})
	user = result.fetchone()

	return user

def get_user_games(user_id):
	
	sql = text(
		"SELECT "
		    "COUNT(DISTINCT g.quiz_id) AS played_quizzes, "
		    "COUNT(DISTINCT g.id) AS played_games, "
		    "COUNT(DISTINCT a.id) AS all_answers, "
		    "COUNT(DISTINCT ca.id) AS correct_answers, "
		    "COALESCE(CAST(CAST(COUNT(DISTINCT ca.id) AS DOUBLE PRECISION) / NULLIF(COUNT(DISTINCT a.id), 0) * 100 AS INTEGER), 0) AS correct_answer_percent "
		"FROM "
		    "users AS u "
		"LEFT JOIN games AS g ON "
		    "g.user_id = u.id "
		"LEFT JOIN answers AS a ON "
		    "a.game_id = g.id "
		"LEFT JOIN answers AS ca ON "
		    "ca.game_id = g.id "
		    "AND ca.is_correct = True "
		"WHERE "
		    "u.id = :user_id"
		";"
	)
	result = db.session.execute(sql, {"user_id":user_id})
	games = result.fetchone()

	return games

def get_user_quizzes(user_id):

	sql = text(
		"SELECT " 
		    "COUNT(DISTINCT q.id) AS created_quizzes, " 
		    "COUNT(DISTINCT g.id) AS created_quizzes_played_games, " 
		    "r.reviews, " 
		    "COALESCE(CAST(r.total_grade AS DOUBLE PRECISION) / NULLIF(r.reviews, 0), 0) AS rating " 
		"FROM " 
		    "users AS u " 
		"LEFT JOIN quizzes AS q ON  " 
		    "q.creator_id = u.id " 
		"LEFT JOIN games AS g ON " 
		    "g.quiz_id = q.id " 
		"LEFT JOIN ( " 
		    "SELECT " 
		        "quiz_id, " 
		        "COUNT(*) AS reviews, " 
		        "SUM(grade) AS total_grade " 
		    "FROM " 
		        "reviews " 
		    "GROUP BY " 
		        "quiz_id " 
		    ") AS r ON r.quiz_id = q.id " 
		"WHERE " 
		    "u.id = :user_id " 
		"GROUP BY " 
		    "u.id, " 
		    "r.reviews, " 
		    "r.total_grade " 
		";" 
	)
	result = db.session.execute(sql, {"user_id":user_id})
	quizzes = result.fetchone()

	return quizzes