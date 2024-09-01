Sovelluksen toiminnallisuudet
-

Sovelluksessa voi luoda omia visoja ja pelata valmiita esimerkkivisoja.

Visoissa on viisi kysymystä, ja jokaisella kysymyksellä on neljä vastausvaihtoehtoa. Yksi näistä vaihtoehdoista on oikein.

Visan pelaamisen jälkeen sen voi arvostella (arvosana 1-5) ja jättää kommentin visasta.

Omia pelien ja luotujen visojen tilastoja voi tutkia omasta profiilista.

Ulkoasu
-

Ulkoasua kehitetty aiemmasta. Ei kovin yhtenäinen ja edelleen keskeneräinen.

Käynnistysohjeet
-
Sovellusta ei ole viety tuotantoon, vaan sen testaaminen onnistuu vain lokaalisti.

- Kloonaa repositorio koneellesi
- Navigoi komentokehotteessa kloonaamasi repositorion kansioon
- Suorita seuraavat komennot alustaaksesi virtuaaliympäristö ja vaadittavat ohjelmat
	- python3 -m venv venv
   	- source venv/bin/activate
   	- pip install -r ./requirements.txt
- Lataa tietokannan malli seuraavalla komennolla. Malli sisältää testidataa, jonka tarkoituksena on helpottaa pelaamisen ja ulkoasun arviointia ja testaamista.
	- psql < schema.sql
   	- On suositeltavaa alustaa erillinen tietokanta, jos yleisiä taulukkonimiä, kuten users, on käytössä omissa ennaltamääritellyissä tietokannoissa.
  	- Tässä tapauksessa käytä komentoa psql tsoha-visa < schema.sql
  	- Käynnistä tietokanta erillisessä komentokehotteessa komennolla start-pg.sh
 - Aja seuraava komento käynnistääksesi virtuaaliympäristön testausta varten
	- flask run
