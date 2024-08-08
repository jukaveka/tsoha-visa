CREATE TABLE users (id SERIAL PRIMARY KEY, nickname TEXT, password TEXT, role TEXT);

CREATE TYPE quiz_category AS ENUM ('Sport', 'TV and Movies', 'Music', 'Video games', 'Literature', 'Politics', 'Geography', 'History', 'Business', 'Technology', 'General', 'Science', 'Math', 'Biology', 'Culinary', 'Culture', 'Trivia');

CREATE TABLE quizzes (id SERIAL PRIMARY KEY, creator_id INTEGER REFERENCES users, name TEXT, category quiz_category);

CREATE TABLE questions (id SERIAL PRIMARY KEY, quiz_id INTEGER REFERENCES quizzes, question TEXT);

CREATE TABLE choices (id SERIAL PRIMARY KEY, question_id INTEGER REFERENCES questions, choice TEXT, is_correct BOOLEAN);

CREATE TABLE answers (ID SERIAL PRIMARY KEY, quiz_id INTEGER REFERENCES quizzes, question_id INTEGER REFERENCES questions, choice_id INTEGER REFERENCES choices, is_correct BOOLEAN);
