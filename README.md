Sovelluksen toiminnallisuudet
-

Sovelluksessa voi luoda omia visoja ja pelata valmiita esimerkkivisoja.

Visoissa on viisi kysymystä, ja jokaisella kysymyksellä on neljä vastausvaihtoehtoa. Yksi näistä vaihtoehdoista on oikein.

Visan pelaamisen jälkeen sen voi arvostella (arvosana 1-5) ja jättää kommentin visasta.

Omia pelien ja luotujen visojen tilastoja voi tutkia omasta profiilista.

Alkuperäisestä suunnitelmasta puuttuu alkuperäisin suunnitellut vaikeustasot ja vinkit. Tarkoituksena lisätä kuva-mahdollisuudet vähintään visoille.

Ulkoasu
-

Ulkoasu on hyvin pelkistetty ja vaihtelee sivutasolla. Lopullinen, yhtenäistetty ulkoasu on suunnitteluvaiheessa. Alla liitettynä tämän hetken prototyyppi index-sivun ulkoasusta.

![image](https://github.com/user-attachments/assets/24c642be-d377-4f4e-be7c-85429d82d6f5)

Käynnistysohjeet
-

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
