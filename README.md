Track watched movies and TV-series

Sovelluksen avulla käyttäjä voi seurata mitä elokuvia ja sarjoja on katsonut ja antaa niille arvioita. Käyttäjä voi myös lisätä listalle seuraavaksi katsottavat elokuvat ja sarjat.

Toiminnallisuuksia:

Versio 1.0

- Käyttäjä voi luoda uuden tunnuksen ja kirjautua sisään ja ulos.
- Käyttäjä voi hakea elokuvaa/sarjaa sen nimellä.
- Käyttäjä voi lisätä uuden elokuvan tai sarjan tietokantaan.
- Käyttäjä voi lisätä omalle listalleen seuraavana katsottavissa olevat elokuvat ja sarjat.
- Käyttäjä voi poistaa omalta listalta elokuvan/sarjan
- Käyttäjä voi merkata elokuvan/sarjan katsotuksi
- Käyttäjä näkee mitkä elokuvat/sarjat on katsonut
- Käyttäjä voi antaa arvion elokuvalle/sarjalle
- Käyttäjä voi muokata antamaansa arviota.


To do:
- Käyttäjä näkee etusivulla tilaston montako elokuvaa/tuotantokautta sarjoista on katsonut.
- Käyttäjä näkee etusivulla kaikkien antamiensa arvosanojen keskiarvon.
- Käyttäjä näkee etusivulla top 3 parhaimmat arviot saaneet elokuvat/sarjat.

Voit testata sovellusta paikallisesti:
1. Kloonaa tämä repositorio omalle koneelle ja siirry juurikansioon
2. Luo kansioon .env-tiedosto, jossa\
    DATABASE_URL= tietokannan-paikallinen-osoite\
    SECRET_KEY= salainen-avain
    
    Esim. voit luoda oman salaisen avaimen komennoilla:\
        $ python3\
        >>> import secrets\
        >>> secrets.token_hex(16)

3. Aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla\
    $ python3 -m venv venv\
    $ source venv/bin/activate\
    $ pip install -r ./requirements.txt

4. Käynnistä taustalle tietokanta ja hae sitten tietokannan skeema komennolla\
    $ psql < schema.sql

5. Käynnistä sovellus komennolla\
    $ flask run
