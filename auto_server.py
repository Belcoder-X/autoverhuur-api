from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel

app = FastAPI()


class Auto(BaseModel):
    modelnaam: str
    dagprijs: int
    aantal: int

class Verhuur(BaseModel):
    klantnaam: str
    automodel: str
    dagen: int


@app.post("/voeg_toe")
def toevoegen(auto:Auto):
    connection = sqlite3.connect("verhuur.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS autos (modelnaam, dagprijs, aantal)")
    cursor.execute("SELECT * FROM autos WHERE modelnaam = ?", (auto.modelnaam,))
    lijst = cursor.fetchone()
    if lijst is not None and lijst[0].strip().lower() == auto.modelnaam.strip().lower():
        return {"status": False, "bericht": "auto is al toegevoegd"}
    else:
        cursor.execute("INSERT INTO autos (modelnaam, dagprijs, aantal) VALUES (?, ?, ?)", (auto.modelnaam, auto.dagprijs, auto.aantal))
        connection.commit()
        connection.close()
        return {"status": True, "bericht": f"{auto.modelnaam} toegevoegd, dagprijs: {auto.dagprijs}euro, aantal: {auto.aantal}"}


@app.post("/huur")
def huren(huur:Verhuur):
    connection = sqlite3.connect("verhuur.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS verhuringen (klantnaam, automodel, dagen, totaal)")
    connection.commit()
    cursor.execute("SELECT * FROM autos WHERE modelnaam = ?", (huur.automodel,))
    lijst = cursor.fetchone()
    if lijst is not None and lijst[0].strip().lower() == huur.automodel.strip().lower() and lijst[2] >= 1:
        cursor.execute("UPDATE autos SET aantal = aantal - 1 WHERE modelnaam = ?", (huur.automodel,))
        totaal = lijst[1] * huur.dagen
        cursor.execute("INSERT INTO verhuringen (klantnaam, automodel, dagen, totaal) VALUES (?, ?, ?, ?)", (huur.klantnaam, huur.automodel, huur.dagen, totaal))
        connection.commit()
        connection.close()
        return {"status": True, "bericht": f"totaal prijs: {totaal}"}
    else:
        return {"status": False, "bericht": "foute auto_model"}


@app.get("/kijk")
def kijk():
    connection = sqlite3.connect("verhuur.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM verhuringen")
    lijst = cursor.fetchall()
    connection.close()
    return lijst

@app.get("/autos")
def autos():
    connection = sqlite3.connect("verhuur.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM autos")
    lijst = cursor.fetchall()
    connection.close()
    return lijst