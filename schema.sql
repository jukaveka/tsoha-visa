CREATE TABLE users (id SERIAL PRIMARY KEY, nickname TEXT, password TEXT, role TEXT);

CREATE TYPE quiz_category AS ENUM ('Sports', 'TV and Movies', 'Music', 'Video games', 'Literature', 'Politics', 'Geography', 'History', 'Business', 'Technology', 'General', 'Science', 'Math', 'Biology', 'Culinary', 'Culture', 'Trivia');

CREATE TABLE quizzes (id SERIAL PRIMARY KEY, creator_id INTEGER REFERENCES users, name TEXT, category quiz_category);

CREATE TABLE questions (id SERIAL PRIMARY KEY, quiz_id INTEGER REFERENCES quizzes, question TEXT);

CREATE TABLE choices (id SERIAL PRIMARY KEY, question_id INTEGER REFERENCES questions, choice_number INTEGER, choice TEXT, is_correct BOOLEAN);

CREATE TABLE answers (ID SERIAL PRIMARY KEY, quiz_id INTEGER REFERENCES quizzes, question_id INTEGER REFERENCES questions, choice_id INTEGER REFERENCES choices, is_correct BOOLEAN);

INSERT INTO users (nickname, password) VALUES ('Juhani', 'scrypt:32768:8:1$euuGzsLJhflrI1Kh$e6897de0f857a2231808853c1
1027302dd3e8e366da88abcbe3106dcf39cf2d68a7f05236b4aa07f43572131e21fe95a4a072957e
2dcc5df331035512a9e6c34');
INSERT INTO users (nickname, password) VALUES ('Tero', 'scrypt:32768:8:1$euuGzsLJhflrI1Kh$e6897de0f857a2231808853c1
1027302dd3e8e366da88abcbe3106dcf39cf2d68a7f05236b4aa07f43572131e21fe95a4a072957e
2dcc5df331035512a9e6c34');

INSERT INTO quizzes (creator_id, name, category) VALUES (1, 'Snookervisa', 'Sports');
INSERT INTO quizzes (creator_id, name, category) VALUES (2, 'Videopelivisa', 'Video games'); 
INSERT INTO quizzes (creator_id, name, category) VALUES (1, 'NHL-visa', 'Sports');

INSERT INTO questions (quiz_id, question) VALUES (1, 'Kuka voitti ensimmäisen Snookerin maailmanmestaruuden vuonna 1927?');
INSERT INTO questions (quiz_id, question) VALUES (1, 'Ensimmäinen Ison-Britannian ulkopuolinen voittaja, Horace Lindrum, nähtiin vuonna 1952. Mistä maasta hän on kotoisin?');
INSERT INTO questions (quiz_id, question) VALUES (1, 'Maksimibreikki, eli 147 pistettä putkeen, nähtiin ensimmäistä kertaa televisiossa vuonna 1982. Ketä suoritti kyseisen breikin?');
INSERT INTO questions (quiz_id, question) VALUES (1, 'Stephen Hendry dominoi lajia 1990-luvulla, voittaen 7 mestaruutta vuosikymmenen aikana. Mutta kuka pelaaja hävisi finaalissa ensimmäiset viisi vuotta putkeen?');
INSERT INTO questions (quiz_id, question) VALUES (1, 'Ronnie OSullivan on tehnyt kaikkien aikojen nopeimman maksimibreikin vuonna 1997. Missä ajassa breikki tehtiin?');

INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (1, 1, 'Tom Dennis', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (1, 2, 'Fred Lawrence', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (1, 3, 'Clark Mcconachy', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (1, 4, 'Joe Davis', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (2, 1, 'Australia', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (2, 2, 'Irlanti', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (2, 3, 'Uusi-Seelanti', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (2, 4, 'Tanska', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (3, 1, 'Alex Higgins', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (3, 2, 'Steve Davis', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (3, 3, 'Ray Reardon', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (3, 4, 'Dennis Taylor', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (4, 1, 'Ken Doherty', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (4, 2, 'Jimmy White', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (4, 3, 'John Parrott', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (4, 4, 'Peter Ebdon', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (5, 1, '5.29', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (5, 2, '5.08', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (5, 3, '3.58', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (5, 4, '6.25', False);

INSERT INTO questions (quiz_id, question) VALUES (2, 'Mikä on ensimmäinen videopeli, joka on tuonut ne laajempaan tietoisuuteen?'); 
INSERT INTO questions (quiz_id, question) VALUES (2, 'Super Mario Bros. -pelin nähdään pelastaneen peliteollisuuden, mutta mikä peli oli suurin yksittäinen syy vuoden 1983 videopeliteollisuuden romahtamisessa?'); 
INSERT INTO questions (quiz_id, question) VALUES (2, 'Nykyään huippusuosittu Counter-Strike oli alunperin toisen pelin pohjalle rakennettu modi. Mikä peli oli kyseessä?'); 
INSERT INTO questions (quiz_id, question) VALUES (2, 'Mikä oli suomalaisen pelitalo Remedyn ensimmäinen julkaisu?'); 
INSERT INTO questions (quiz_id, question) VALUES (2, 'Mikä videopelisarja yhdistelee Nintendon ja muiden pelitalojen suosituimpia hahmoja samaan tappelupeliin?');

INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (6, 1, 'Space Invader', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (6, 2, 'Tetris', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (6, 3, 'Pong', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (6, 4, 'Pac-Man', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (7, 1, 'E.T.', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (7, 2, 'Donkey Kong', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (7, 3, 'Star Wars', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (7, 4, 'Galaga', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (8, 1, 'Doom', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (8, 2, 'Quake II', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (8, 3, 'Quake', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (8, 4, 'Half-Life', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (9, 1, 'Max Payne', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (9, 2, 'Death Rally', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (9, 3, 'Alan Wake', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (9, 4, 'Quantum Break', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (10, 1, 'Mario Party', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (10, 2, 'Super Smash Bros.', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (10, 3, 'Mario Kart', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (10, 4, 'Tekken', False);

INSERT INTO questions (quiz_id, question) VALUES (3, 'Kuinka monta joukkuetta oli liigan perustamiskaudella mukana?'); 
INSERT INTO questions (quiz_id, question) VALUES (3, 'Kuka oli ensimmäinen pelaaja, joka ylitti 100 pisteen rajan kaudessa?'); 
INSERT INTO questions (quiz_id, question) VALUES (3, 'Wayne Gretzky johtaa kaikkien aikojen pistepörssiä, mutta kuka on listalla toisena?'); 
INSERT INTO questions (quiz_id, question) VALUES (3, 'Kuka pelaaja kieltäytyi pelaamasta hänet varanneessa joukkueessa, ja vaati siirtoa, joka yhdistyy vielä tänäkin päivänä tapahtuviin siirtoihin?'); 
INSERT INTO questions (quiz_id, question) VALUES (3, 'Kuka oli ensimmäinen eurooppalainen, joka voitti kapteenina Stanley Cupin?');

INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (11, 1, '6', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (11, 2, '5', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (11, 3, '7', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (11, 4, '4', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (12, 1, 'Bobby Orr', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (12, 2, 'Gordie Howe', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (12, 3, 'Jean Beliveau', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (12, 4, 'Phil Esposito', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (13, 1, 'Gordie Howe', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (13, 2, 'Mario Lemieux', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (13, 3, 'Jaromir Jagr', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (13, 4, 'Mark Messier', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (14, 1, 'Matt Sundin', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (14, 2, 'Eric Lindros', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (14, 3, 'Steve Yzerman', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (14, 4, 'Vincent Lecavalier', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (15, 1, 'Nicklas Lidström', True);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (15, 2, 'Aleksander Barkov', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (15, 3, 'Jaromir Jagr', False);
INSERT INTO choices (question_id, choice_number, choice, is_correct) VALUES (15, 4, 'Alex Ovechkin', False);