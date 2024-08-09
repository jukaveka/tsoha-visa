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

