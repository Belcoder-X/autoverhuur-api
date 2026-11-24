import pandas as pd
from sklearn.linear_model import LinearRegression
from fastapi import FastAPI
from pydantic import BaseModel
    
data = {"m2": (50, 60, 80, 100, 120, 150), "kamers": (1, 2, 3, 4, 5, 6), "prijs": [120000, 180000, 240000, 290000, 350000, 440000]}

tabel = pd.DataFrame(data)

x = tabel[["m2", "kamers"]]
y = tabel["prijs"]

model = LinearRegression()
model.fit(x, y)


app = FastAPI()

class Huis(BaseModel):
    m2: int
    kamers: int

@app.post("/voorspel")

def voorspel(spel: Huis):
    nieuw_huis = pd.DataFrame({"m2": [spel.m2], "kamers": [spel.kamers]})
    voorspelling = model.predict(nieuw_huis)
    return {"bericht": f"Voorspelde prijs voor {spel.m2} met {spel.kamers}: ${int(voorspelling[0])}"}